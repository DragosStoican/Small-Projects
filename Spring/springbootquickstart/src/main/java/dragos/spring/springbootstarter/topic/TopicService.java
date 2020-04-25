package dragos.spring.springbootstarter.topic;

import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

@Service
public class TopicService {

    List<Topic> topics = new ArrayList<>(Arrays.asList(
            new Topic("spring", "Spring Framework", "Spring Framework Description"),
            new Topic("java", "Core Java", "Core Java Description"),
            new Topic("javascript", "JavaScript", "JavaScript Description")
            ));

    public List<Topic> getAllTopics() {
        return topics;
    }

    public Topic getTopic(String id) {
        return topics.stream().filter(t -> t.getId().equals(id)).findFirst().get();
    }

    public void addTopic(Topic topic) {
        topics.add(topic);
    }

    public void updateTopic(String id, Topic topic) {
        for (Topic t : topics) {
            if(t.getId().equals(id))
            {
                int i = topics.indexOf(t);
                topics.set(i, topic);
                return;
            }
        }

    }

    public void deleteTopic(String id) {
        /*for (Topic t : topics) {
            if(t.getId().equals(id))
            {
                topics.remove(t);
                return;
            }
        }*/
        // Lambda predicate method
        topics.removeIf(t -> t.getId().equals(id));
    }
}
