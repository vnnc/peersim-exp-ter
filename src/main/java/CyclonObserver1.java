import cyclon.Cyclon;
import observers.DictGraph;
import observers.ObserverProgram;
import peersim.config.Configuration;
import peersim.core.CommonState;
import peersim.core.Network;
import peersim.core.Node;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Random;

public class CyclonObserver1 implements ObserverProgram {

    private boolean initialized = false;
    private FileWriter fileWriter;
    private BufferedWriter writer;
    private int cacheSize = Configuration.getInt("protocol.myprotocol.c");
    private int networkSize = Configuration.getInt("SIZE");
    private int nbCycles = Configuration.getInt("CYCLES");
    private int shuffleInterval;

    public CyclonObserver1(String prefix){
        this.shuffleInterval = Configuration.getInt(prefix+".shuffleInterval");
    }

    public void tick(long currentTick, DictGraph observer) {
        if(currentTick == 0){
            try {
                init(observer);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        else{
            if(initialized){
                observe(currentTick,observer);
            }else{
                checkInit(currentTick);
            }
        }
    }

    private void checkInit(long currentTick)
    {
        if (currentTick > 100) {
            initialized = true;
        }
    }

    public void observe(long currentTick, DictGraph observer){
        List<Node> partialView = ((Cyclon) observer.nodes.get(Network.get(0).getID()).pss).getPeers(Integer.MAX_VALUE);
        int randomPeer = getRandomFromNodes(partialView);

        if(currentTick%shuffleInterval == 0)
        try {
            writer.write(networkSize+","+nbCycles+","+shuffleInterval+","+randomPeer);
            writer.write(System.getProperty("line.separator"));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private int getRandomFromNodes(List<Node> nodes){
        return nodes.get(CommonState.r.nextInt(nodes.size())).getIndex();
    }

    public void onLastTick(DictGraph observer) {
        try {
            writer.close();
            fileWriter.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void init(DictGraph observer) throws IOException {
        Long timestamp = new Date().getTime();
        this.fileWriter = new FileWriter("samples/samples_"+timestamp+".csv",false);
        this.writer = new BufferedWriter(fileWriter);

        writer.write("NETSIZE,NB_CYCLES,SHUFFLE_INTERVAL,PEERID");
        writer.write(System.getProperty("line.separator"));
    }
}
