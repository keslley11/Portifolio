class Animal { 

    String nome;
    int idade;

    // Construtor
    public Animal(String nome, int idade) {
        this.nome = nome;
        this.idade = idade;
    }
    public void emitirSom() { 
        System.out.println("Som genérico de animal..."); 
    }
    // Método para comer
    public void comer() {
        System.out.println(this.nome + " está comendo.");
    }
    // Método para dormir
    public void dormir() {
        System.out.println(this.nome + " está dormindo.");
    }
}
// Subclasse (herdando de Animal)
class Mamifero extends Animal {
    boolean temPelos;

    // Construtor
    public Mamifero(String nome, int idade, boolean temPelos) {
        super(nome, idade);  // Chama o construtor da superclasse (Animal)
        this.temPelos = temPelos;
    }
    // Método para verificar pelos
    public void getPelos() {
        if(temPelos) System.out.println(this.nome + " tem pelos.");
        else System.out.println(this.nome + " não tem pelos.");
    }

    // Método sobrescrito para emitir som
    @Override
    public void emitirSom() {
        System.out.println(this.nome + " faz som de mamífero.");
    }
}
    
class Cachorro extends Mamifero {
    String raca;

    // Construtor
    public Cachorro(String nome, int idade, boolean temPelos, String raca) {
        super(nome, idade, temPelos);  // Chama o construtor da superclasse (Mamifero)
        this.raca = raca;
    }

    // Método específico para Cachorro
    public void latir() {
        System.out.println(this.nome + " está latindo: au-au.");
    }

    // Método sobrescrito para emitir som
    @Override
    public void emitirSom() {
        latir();
    }
    // Método sobrescrito para comer
    @Override
    public void comer() {
        System.out.println(this.nome + " está comendo (carne ou vegetais).");
    }
} 

class Felino extends Mamifero {
    String especie;

    // Construtor
    public Felino(String nome, int idade, boolean temPelos, String especie) {
        super(nome, idade, temPelos);  // Chama o construtor da superclasse (Mamifero)
        this.especie = especie;
    }

    // Método específico para Felinos
    public void rugir() {
        System.out.println(this.nome + " está rugindo: miau-miau.");
    }

    // Método sobrescrito para emitir som
    @Override
    public void emitirSom() {
        rugir();
    }
    // Método sobrescrito para comer
    @Override
    public void comer() {
        System.out.println(this.nome + " está comendo (carne).");
    }
} 
    

    
    public class Main { 
        public static void main(String[] args) { 

            Animal animalGenerico = new Animal("Tom",3);
            Mamifero roedor = new Mamifero("ratatui", 2, true);
            Cachorro meuCachorro = new Cachorro("Lessie",4,true,"Vira-lata");
            Felino gato = new Felino("Tom",1,true,"Siamês");
            Felino tigre = new Felino("Diego",6,true,"dente-de sabre");
           
            // Chamando métodos
            animalGenerico.emitirSom();
            animalGenerico.comer();
            animalGenerico.dormir();

            roedor.emitirSom();
            roedor.comer();
            roedor.dormir();
            roedor.getPelos();

            meuCachorro.emitirSom();
            meuCachorro.comer();
            meuCachorro.dormir();
            meuCachorro.getPelos();
            meuCachorro.latir();

            tigre.emitirSom();
            tigre.comer();
            tigre.dormir();
            tigre.getPelos();
            tigre.rugir();
        } 
   } 
 