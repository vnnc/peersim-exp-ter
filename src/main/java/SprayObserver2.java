import observers.DictGraph;
import observers.ObserverProgram;
import peersim.config.Configuration;
import peersim.core.Network;
import peersim.core.Node;
import spray.Spray;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Random;

public class SprayObserver2 implements ObserverProgram {

    private boolean initialized = false;
    private FileWriter fileWriter;
    private BufferedWriter writer;
    private int cacheSize = Configuration.getInt("protocol.myprotocol.c");
    private int networkSize = Configuration.getInt("SIZE");
    private int nbCycles = Configuration.getInt("CYCLES");
    private int shuffleInterval;
    private ArrayList<Node> previousView;


    public SprayObserver2(String prefix) {
        this.shuffleInterval = Configuration.getInt(prefix+".shuffleInterval");
    }

    @Override
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
                checkInit(observer);
            }
        }
    }

    private void checkInit(DictGraph observer)
    {
        List<Node> partialView = ((Spray) observer.nodes.get(Network.get(0).getID()).pss).getPeers(Integer.MAX_VALUE);
        if(partialView.size() > 1){
            initialized = true;
        }
    }

    public void observe(long currentTick, DictGraph observer){
        List<Node> partialView = ((Spray) observer.nodes.get(Network.get(0).getID()).pss).getPeers(Integer.MAX_VALUE);
        ArrayList<Integer> newPeers = getChangedNodes(partialView);
        previousView = new ArrayList<>(partialView);

        if(currentTick%shuffleInterval == 0) {
            try {
                for (Integer i : newPeers) {
                    writer.write(networkSize + "," + nbCycles + "," + shuffleInterval + "," + i);
                    writer.write(System.getProperty("line.separator"));
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    private ArrayList<Integer> getChangedNodes(List<Node> nodes){

        ArrayList<Integer> result = new ArrayList<>();

        for(Node node : nodes){
            if(!previousView.contains(node)){
                result.add(node.getIndex());
            }
        }

        return result;
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
        previousView = new ArrayList<>();
        Long timestamp = new Date().getTime();
        this.fileWriter = new FileWriter("samples/samples_"+timestamp+".csv",false);
        this.writer = new BufferedWriter(fileWriter);

        writer.write("NETSIZE,NB_CYCLES,SHUFFLE_INTERVAL,PEERID");
        writer.write(System.getProperty("line.separator"));
    }
}
