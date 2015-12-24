package indi.tamvm.blog;

import akka.actor.Props;
import akka.actor.UntypedActor;
import akka.actor.ActorRef;

public class AppAkka
    extends UntypedActor{

    @Override
    public void preStart(){
        final ActorRef greeter =
            getContext().actorOf(Props.create(AkkaGreeter.class), "greeter"); 
        greeter.tell(AkkaGreeter.Msg.GREET, getSelf()); 
    }

    @Override
    public void onReceive(Object msg){
        if (msg == AkkaGreeter.Msg.DONE){
            getContext().stop(getSelf()); 
        }
        else{
            unhandled(msg); 
        }
    }
}
