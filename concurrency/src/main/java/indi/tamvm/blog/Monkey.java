package indi.tamvm.blog; 

public class Monkey implements Runnable{

    Tree tree; 
    public Monkey(Tree tree){
        this.tree = tree; 
    }

    public void run(){
        try{
            for(int i = 0; i <= 10; i++){
                Thread.sleep(10); 
                this.tree.drop();
            }
        }
        catch(InterruptedException e){

        }
    }

}
