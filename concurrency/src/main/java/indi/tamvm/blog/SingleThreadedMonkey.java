package indi.tamvm.blog; 
import java.util.concurrent.*;

public class SingleThreadedMonkey implements Runnable{

    static ExecutorService executor = Executors.newSingleThreadExecutor(); 

    Tree tree; 
    public Monkey(Tree tree){
        this.tree = tree; 
    }

    public void run(){
        try{
            for(int i = 0; i <= 10; i++){
                Thread.sleep(10); 
                drop(); 
            }
        }
        catch(InterruptedException e){

        }
    }

    private void drop(){
        executor.submit(
                new Callable<Void>(){
                    public Void call() throws InterruptedException {
                        tree.drops();
                    }
                }
        );
    }

}
