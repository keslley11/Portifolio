import java.util.Scanner;

class ContaBancaria { 
    private String titular;
    private String password; 
    private double saldo; 
    
    public ContaBancaria(String titular, String pass) { 
        this.titular = titular; 
        this.saldo = 0.0;
        this.password = pass;
    } 
    
    public void depositar(double valor) { 
        saldo += valor; 
    } 
    
    public void sacar(double valor) {  // somente com senha (access)
        if (saldo >= valor) saldo -= valor; 
        else System.out.println("Saldo insuficiente!"); 
    } 
    
    public void mostrarSaldo() {  // somente com senha (access)
        System.out.println("Saldo de " + titular + ": R$" + saldo); 
    }

    // Métodos de acesso à conta
    public String getTitular() {
        return titular;
    }
    public String getPassword() {
        return password;
    }
}

public class Main { 

    public static ContaBancaria[] addAccount(int n, ContaBancaria arr[])
    {
        Scanner scanner = new Scanner(System.in);
        System.out.print("\nEnter the Name: ");
        String titular = scanner.next();
        System.out.print("\nEnter the Password: ");
        String pass = scanner.next();
        scanner.nextLine();
        ContaBancaria conta = new ContaBancaria(titular,pass); //cria conta

        ContaBancaria newarr[] = new ContaBancaria[n+1];
        // insert the elements from
        // the old array into the new array
        // insert all elements till n
        // then insert x at n+1
        for(int i = 0; i < n; i++)
            newarr[i] = arr[i];
        newarr[n] = conta;          //add conta
        return newarr;
    }

    public static void accessAccount(int n, ContaBancaria arr[])
    {
        Scanner scanner = new Scanner(System.in);
        System.out.print("\nEnter the Name: ");
        String input_titular = scanner.next();

        //encontra a conta
        int index_account=-1;
        for(int i = 0; i < n; i++)
            if(arr[i].getTitular().equalsIgnoreCase(input_titular)){
                index_account=i;
                break;
            }
        if(index_account==-1){
            System.out.print("\nNão encontrado!");
            return;
        }

        //verifica senha
        System.out.print("\nEnter the Password: ");
        String input_pass = scanner.next();
        if(!arr[index_account].getPassword().equals(input_pass)){
            System.out.print("\nSenha incorreta!");
            return;
        }

        //acesso concedido para sacar e mostrar
        int menu;
        while (true) {
                
            System.out.println("\nSelecione:\n");
            System.out.println("\tSacar --> 1 ");
            System.out.println("\tMostrar saldo --> 2 ");
            System.out.println("\tVoltar --> 3 ");
            menu = scanner.nextInt();
            scanner.nextLine();

            switch(menu) {
                case 1:
                    System.out.print("Value (ex: 0,99): ");
                    double value = scanner.nextDouble();
                    scanner.nextLine();
                    arr[index_account].sacar(value);
                    break;
                case 2:
                    arr[index_account].mostrarSaldo();
                    break;
                case 3:
                    System.out.println("\nreturning ...");
                    return;
                
                default:
                    System.out.println("Invalid, try again...");
            }
        }
    }
    public static void main(String[] args) { 

        ContaBancaria conta_k = new ContaBancaria("Keslley", "1234"); 
        conta_k.depositar(100); 
        //conta_k.sacar(30); 
        //conta_k.mostrarSaldo(); 

        ContaBancaria[] Accounts = {conta_k};// add "Keslley" a lista   (default)
        int n_accounts = 1;
        
        
        Scanner scanner = new Scanner(System.in);
        int menu;
        while (true) {
                
            System.out.println("\nMenu:\n");
            System.out.println("\tCreate Account --> 1 ");
            System.out.println("\tAccess Account --> 2 ");
            System.out.println("\tExit --> 3 ");
            menu = scanner.nextInt();
            scanner.nextLine();

            switch(menu) {
                case 1:
                    Accounts = addAccount(n_accounts++,Accounts);
                    break;
                case 2:
                    accessAccount(n_accounts,Accounts);
                    break;
                case 3:
                    System.out.println("\nExiting ...");
                    scanner.close();
                    return;
                
                default:
                    System.out.println("Invalid, try again...");
            }
            
        }
    } 
}