package indi.tamvm.blog;

import akka.actor.Props;
import akka.actor.UntypedActor;
import akka.actor.ActorRef;

public class AkkaGreeter
    extends UntypedActor{
    public static enum Msg {
        GREET, DONE;
    }

    public void onReceive(Object msg){
        if(msg == Msg.GREET){
            System.out.println("HELLO"); 
            getSender().tell(Msg.DONE, getSelf()); 
        }
        else{
            unhandled(msg); 
        }
    }
}
