package indi.tamvm.blog;

/**
 *
 */
public class App 
{
    public static void main( String[] args )
    {
        Tree tree = new Tree(10); 
        Thread m1 = new Thread(new Monkey(tree)); 
        Thread m2 = new Thread(new Monkey(tree)); 
        m1.start(); 
        m2.start();
        
    }
}
