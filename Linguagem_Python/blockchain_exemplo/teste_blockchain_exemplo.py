import unittest
from blockchain_exemplo import Blockchain, Transaction, generate_keys
from ecdsa import SigningKey, VerifyingKey, SECP256k1

class TestBlockchain(unittest.TestCase):

    def setUp(self):
        """Configuração inicial para os testes"""
        self.blockchain = Blockchain()
        self.sender_key, self.sender_verifying_key = generate_keys()
        self.receiver_key, self.receiver_verifying_key = generate_keys()

    def test_valid_transaction(self):
        """Teste de uma transação válida"""
        transaction = Transaction(self.sender_verifying_key.to_string().hex(), self.receiver_verifying_key.to_string().hex(), 50)
        transaction.sign_transaction(self.sender_key)
        self.assertTrue(transaction.is_valid(), "Transação válida foi considerada inválida")

    def test_fraudulent_transaction(self):
        """Teste de uma transação fraudulenta"""
        transaction = Transaction(self.sender_verifying_key.to_string().hex(), self.receiver_verifying_key.to_string().hex(), 50)
        transaction.sign_transaction(self.sender_key)

        fraudulent_transaction = Transaction(self.sender_verifying_key.to_string().hex(), self.receiver_verifying_key.to_string().hex(), 100)
        fraudulent_transaction.signature = transaction.signature  # Copiar assinatura
        self.assertFalse(fraudulent_transaction.is_valid(), "Transação fraudulenta foi considerada válida")

    def test_unsigned_transaction(self):
        """Teste de uma transação sem assinatura"""
        transaction = Transaction(self.sender_verifying_key.to_string().hex(), self.receiver_verifying_key.to_string().hex(), 50)
        self.assertFalse(transaction.is_valid(), "Transação sem assinatura foi considerada válida")

    def test_invalid_key_transaction(self):
        """Teste de uma transação com chave pública inválida"""
        invalid_key_transaction = Transaction("chave_publica_invalida", self.receiver_verifying_key.to_string().hex(), 50)
        invalid_key_transaction.signature = "assinatura_falsa"
        self.assertFalse(invalid_key_transaction.is_valid(), "Transação com chave pública inválida foi considerada válida")

    def test_add_transaction_to_invalid_chain(self):
        self.blockchain.chain[0].hash = "hash_incorreto"  # Corrompe a blockchain
        transaction = Transaction(self.sender_verifying_key.to_string().hex(), self.receiver_verifying_key.to_string().hex(), 50)
        transaction.sign_transaction(self.sender_key)
        #with self.assertRaises(ValueError):
        #    self.blockchain.add_transaction(transaction)
        self.assertFalse(self.blockchain.add_transaction(transaction))

    def test_mine_on_invalid_chain(self):
        self.blockchain.chain[0].hash = "hash_incorreto"  # Corrompe a blockchain
        #with self.assertRaises(ValueError):
        #    self.blockchain.mine_pending_transactions("miner_address")
        self.assertFalse(self.blockchain.mine_pending_transactions("miner_address"))

    def test_blockchain_integrity(self):
        """Teste de integridade da blockchain"""
        transaction = Transaction(self.sender_verifying_key.to_string().hex(), self.receiver_verifying_key.to_string().hex(), 50)
        transaction.sign_transaction(self.sender_key)
        self.blockchain.add_transaction(transaction)
        self.blockchain.mine_pending_transactions("miner_address")
        self.assertTrue(self.blockchain.is_chain_valid(), "Blockchain foi considerada inválida após mineração")

    def test_blockchain_persistence(self):
        """Teste de persistência da blockchain"""
        transaction = Transaction(self.sender_verifying_key.to_string().hex(), self.receiver_verifying_key.to_string().hex(), 50)
        transaction.sign_transaction(self.sender_key)
        self.blockchain.add_transaction(transaction)
        self.blockchain.mine_pending_transactions("miner_address")
        self.blockchain.save_to_file("test_blockchain.json")

        new_blockchain = Blockchain()
        new_blockchain.load_from_file("test_blockchain.json")
        self.assertEqual(len(new_blockchain.chain), len(self.blockchain.chain), "O número de blocos não corresponde após carregar a blockchain")
        self.assertTrue(new_blockchain.is_chain_valid(), "Blockchain carregada foi considerada inválida")

if __name__ == "__main__":
    unittest.main()
