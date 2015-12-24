package indi.tamvm.blog; 

public class Tree{
    private int bananas; 

    public Tree(int b){
        this.bananas = b; 
    }

    public void grows(){
        this.bananas += 1; 
        System.out.println("GROWS " + this.bananas); 
    }

    public void drop(){
        this.bananas -= 1; 
        System.out.println("DROP " + this.bananas); 
    }
}
