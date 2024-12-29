import hashlib
import time
import json
from ecdsa import SigningKey, SECP256k1, VerifyingKey, BadSignatureError
#cd C:\Users\Keslley\gitHub\Portifolio\Linguagem_Python\blockchain_exemplo



# Função para gerar o hash de um bloco
def calculate_hash(block):
    block_string = f"{block['index']}{block['timestamp']}{block['data']}{block['previous_hash']}{block['nonce']}"
    return hashlib.sha256(block_string.encode()).hexdigest()

# Classe para representar um bloco
class Block:
    def __init__(self, index, timestamp, data, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = calculate_hash(self.__dict__)

    # Método para realizar a prova de trabalho (Proof of Work)
    def mine_block(self, difficulty):
        while not self.hash.startswith('0' * difficulty):
            self.nonce += 1
            self.hash = calculate_hash(self.__dict__)

# Classe para representar uma transação
class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender  # Chave pública do remetente em formato hexadecimal
        self.receiver = receiver  # Chave pública do receptor em formato hexadecimal
        self.amount = amount
        self.signature = None

    def sign_transaction(self, signing_key):
        if signing_key.get_verifying_key().to_string().hex() != self.sender:
            raise ValueError("A chave privada não corresponde ao endereço do remetente.\n")

        message = f"{self.sender}{self.receiver}{self.amount}"
        self.signature = signing_key.sign(message.encode()).hex()

    def is_valid(self):
        if self.sender == "0":  # Transações de recompensa (ex.: para mineradores) não precisam de assinatura
            return True

        if not self.signature:
            print("Transação sem assinatura!\n")
            return False

        try:
            verifying_key = VerifyingKey.from_string(bytes.fromhex(self.sender), curve=SECP256k1)
            message = f"{self.sender}{self.receiver}{self.amount}"
            verifying_key.verify(bytes.fromhex(self.signature), message.encode())
            return True
        except BadSignatureError:
            print("Assinatura inválida!\n")
            return False
        except Exception as e:
            print(f"Erro na verificação da transação: {e}\n")
            return False


# Classe para representar a blockchain
class Blockchain:
    def __init__(self, difficulty=4):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.pending_transactions = []
        self.block_size_limit = 5

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, block):
        self.chain.append(block)

    def mine_pending_transactions(self, miner_address):
        if not self.is_chain_valid():
            #raise ValueError("Blockchain inválida, mineração não pode continuar.")
            print("Blockchain inválida, mineração não pode continuar.")
            return False
        if len(self.pending_transactions) == 0:
            print("Nenhuma transação para minerar.\n")
            return #1

        block_data = []
        for transaction in self.pending_transactions:
            if transaction.is_valid():
                block_data.append(transaction.__dict__)

        new_block = Block(len(self.chain), time.time(), block_data, self.get_latest_block().hash)
        new_block.mine_block(self.difficulty)
        self.add_block(new_block)

        print(f"Bloco minerado: {new_block.hash}\n")
        self.pending_transactions = []

    def add_transaction(self, transaction):
        if not transaction.is_valid():
            print("Transação inválida!\n")
            return
        if not self.is_chain_valid():
            #raise ValueError("Blockchain inválida, não é possível adicionar transações.")
            print("Blockchain inválida, não é possível adicionar transações.")
            return False
   
        self.pending_transactions.append(transaction)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != calculate_hash(current_block.__dict__):
                return False
            if current_block.previous_hash != previous_block.hash:
                return False

        return True
    
    '''
    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            json.dump([block.__dict__ for block in self.chain], file)
    
    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            blocks = json.load(file)
            self.chain = [Block(**block) for block in blocks]
    '''

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            json.dump({"chain": [block.__dict__ for block in self.chain]}, file, indent=4)


    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            blocks = data["chain"]

            self.chain = []
            for block in blocks:
                new_block = Block(
                    index=block["index"],
                    timestamp=block["timestamp"],
                    data=block["data"],
                    previous_hash=block["previous_hash"],
                    nonce=block["nonce"]
                )
                new_block.hash = block["hash"]  # Atribuir o hash manualmente
                self.chain.append(new_block)


# Gerar chaves públicas/privadas para transações
                
def generate_keys():
    signing_key = SigningKey.generate(curve=SECP256k1)
    verifying_key = signing_key.get_verifying_key()
    return signing_key, verifying_key

# Testando o código
if __name__ == "__main__":
    blockchain = Blockchain()

    # Gerar chaves para o remetente e receptor
    sender_key, sender_verifying_key = generate_keys()
    receiver_key, receiver_verifying_key = generate_keys()

    
    # Teste 1: Transação válida
    print("\nTeste 1: Transação válida\n")
    transaction = Transaction(sender_verifying_key.to_string().hex(), receiver_verifying_key.to_string().hex(), 50)
    transaction.sign_transaction(sender_key)
    print("Transação válida:", transaction.is_valid(),'\n')  # Deve ser True
    blockchain.add_transaction(transaction)

    # Teste 2: Transação fraudulenta (alteração do valor)
    print("\nTeste 2: Transação fraudulenta - Alteração do valor\n")
    fraudulent_transaction = Transaction(sender_verifying_key.to_string().hex(), receiver_verifying_key.to_string().hex(), 100)
    fraudulent_transaction.signature = transaction.signature  # Copiar a assinatura
    print("Transação fraudulenta válida:", fraudulent_transaction.is_valid(),'\n')  # Deve ser False

    # Teste 3: Transação sem assinatura
    print("\nTeste 3: Transação sem assinatura\n")
    unsigned_transaction = Transaction(sender_verifying_key.to_string().hex(), receiver_verifying_key.to_string().hex(), 50)
    print("Transação sem assinatura válida:", unsigned_transaction.is_valid())  # Deve ser False

    # Teste 4: Transação com chave pública inválida
    print("\nTeste 4: Transação com chave pública inválida\n")
    invalid_key_transaction = Transaction("chave_publica_invalida", receiver_verifying_key.to_string().hex(), 50)
    invalid_key_transaction.signature = transaction.signature
    print("Transação com chave pública inválida válida:", invalid_key_transaction.is_valid(),'\n')  # Deve ser False


    # Minerando as transações
    blockchain.mine_pending_transactions("miner_address")

    # Exibindo a blockchain
    for block in blockchain.chain:
        print(f"\nÍndice: {block.index}")
        print(f"Timestamp: {block.timestamp}")
        print(f"Dados: {block.data}")
        print(f"Hash: {block.hash}")
        print(f"Hash anterior: {block.previous_hash}")

    # Verificando se a blockchain é válida
    if blockchain.is_chain_valid():
        print("\nA Blockchain é válida!")
    else:
        print("\nA Blockchain é inválida!")

    # Salvando a blockchain em um arquivo
    blockchain.save_to_file("blockchain.json")
