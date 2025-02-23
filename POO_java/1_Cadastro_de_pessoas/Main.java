import java.lang.*;
import java.util.*;

class Pessoa { 
    private String nome; 
    private int idade;
    /*add atributo: email */
    private String email; 
    
    public Pessoa(String nome, int idade, String email) { 
        this.nome = nome; 
        this.idade = idade;
        this.email = email;

    } 
    
    public String getNome() { return nome; } 
    public void setNome(String nome) { this.nome = nome; } 
    
    public int getIdade() { return idade; } 
    public void setIdade(int idade) { this.idade = idade; } 
    
    public String getEmail() { return email; } 
    public void setEmail(String email) { this.email = email; } 
    
   }

public class Main { 
        
    // Function to add x in arr
    public static Pessoa[] addX(int n, Pessoa arr[], Pessoa x)
    {

       Pessoa newarr[] = new Pessoa[n+1];
    
       // insert the elements from
       // the old array into the new array
       // insert all elements till n
       // then insert x at n+1
       for(int i = 0; i < n; i++)
           newarr[i] = arr[i];
 
       newarr[n] = x;
 
       return newarr;
    }
    
    public static void print_pessoas(int n, Pessoa arr[])
    {
        System.out.println("\nRegister:\n");
        for(int i = 0; i < n; i++){
            System.out.println("Nome: " + arr[i].getNome());
            System.out.println("Idade: " + arr[i].getIdade());
            System.out.println("Email: " + arr[i].getEmail()+"\n");
        }
    }
    
    public static void main(String[] args) { 
            Pessoa p = new Pessoa("Keslley", 23,"keslley.ramos@ufu.br"); 
            System.out.println("Nome: " + p.getNome());
            System.out.println("Idade: " + p.getIdade());
            System.out.println("Email: " + p.getEmail());

            /* vetor para pessoas */
            /* loop para multiplos cadastros:
                    inserir nome,idade e email */
            /* exibir vetor */
            /* retorna ao loop */

            String p_nome;
            int p_idade;
            String p_email;
            Pessoa[] pessoas = {p};// add "Keslley" a lista   (default)
            int n_pessoas = 1;
         

            Scanner scanner = new Scanner(System.in);
            boolean continueRegister = true;
    
            while (continueRegister) {
                
                System.out.print("\nEnter the Name (or 'x' to exit): ");
                p_nome = scanner.next();

                if (p_nome.toLowerCase().equals("x")) {
                    System.out.println("\nExiting ...");
                    break;
                }

                // Add new "pessoa"
                System.out.print("Enter age: ");
                p_idade = scanner.nextInt();
                System.out.print("Enter email: ");
                p_email = scanner.next();
                
                Pessoa x = new Pessoa(p_nome,p_idade,p_email);
                pessoas = addX(n_pessoas++, pessoas, x);
 
                //Print list_pessoas
                print_pessoas(n_pessoas, pessoas);
                
            }
            
            scanner.close();
        }
   }