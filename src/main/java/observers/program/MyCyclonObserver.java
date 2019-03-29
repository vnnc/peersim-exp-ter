package observers.program;

import cyclon.Cyclon;
import observers.DictGraph;
import observers.ObserverProgram;
import peersim.core.Network;

public class MyCyclonObserver implements ObserverProgram {

    private boolean initialized = false;

    public MyCyclonObserver(String prefix){
        System.out.println("PREFIX: "+prefix);
    }

    public void tick(long currentTick, DictGraph observer) {
        if(currentTick == 0){
            init(observer);
            initialized = true;
        }
        else{
            if(initialized){
                observe(currentTick,observer);
            }
        }
    }

    public void observe(long currentTick, DictGraph observer){
        System.out.println(observer.nodes.get((Cyclon) Network.get(0).getID()));
    }

    private int getRandomFromPartialView(){return 0;}

    public void onLastTick(DictGraph observer) {

    }

    public void init(DictGraph observer){
        System.out.println("INIT");
    }
}
