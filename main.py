import numpy as np
import time
from DLL import DLL  # Import the DLL class from the DLL.py file
import random
from maxheap import maxHeap

class Ad:
    def __init__(self, id, tags):
        self.id = id
        self.tags = tags
        self.score = 0

    def __lt__(self, other):
        return self.score < other.score

class Reel:
    def __init__(self, id, tags):
        self.id = id
        self.tags = tags
        self.score = 0

    def __lt__(self, other):
        return self.score < other.score

class User:
    def __init__(self, num_reels, interests):
        self.num_reels = num_reels
        self.interests = interests
        self.interaction_matrix = np.zeros(num_reels) #graphs used as interaction matrix
        self.favourite_tags_count = np.zeros(len(interests)) #graphs used as interaction matrix
        self.reels_watched = 0
        self.interaction_history = DLL()  # Use the DLL for interaction history

    def interact(self, reel, action):
        interaction = (reel.id, action)
        self.interaction_history.insertLast(interaction)  # Add interaction to DLL
        if action == 'like':
            self.interaction_matrix[reel.id] = 1
            for i, tag in enumerate(self.interests):
                if tag in reel.tags:
                    self.favourite_tags_count[i] += 1
            for tag in reel.tags:
                if tag not in self.interests:
                    self.interests[tag] = 0
                    self.favourite_tags_count = np.append(self.favourite_tags_count, 1)
        elif action == 'dislike':
            self.interaction_matrix[reel.id] = -1
        elif action == 'watched':
            self.interaction_matrix[reel.id] = 0.5
        self.reels_watched += 1

class RecommendationEngine:
    def __init__(self, reels, ads):
        self.reels = reels
        self.ads = ads
        self.suggested_reels = set()
        self.suggested_ads = set()
        self.reel_heap = maxHeap()  # Use maxHeap for reels
        self.ad_heap = maxHeap()  # Use maxHeap for ads

    def recommend_reel(self, user):
        for reel in self.reels:
            if reel.id not in self.suggested_reels:
                interest_weight = sum(user.interests.get(tag, 0) * user.favourite_tags_count[i]
                                      for i, tag in enumerate(user.interests) if tag in reel.tags)
                interaction_score = user.interaction_matrix[reel.id]
                weighted_sum = interest_weight + interaction_score
                self.reel_heap.insert_element(reel.id, weighted_sum)

        while True:
            if not self.reel_heap.root:
                self.suggested_reels.clear()
                return self.recommend_reel(user)
            _, reel_id = self.reel_heap.extract_max()
            if reel_id not in self.suggested_reels:
                self.suggested_reels.add(reel_id)
                return next(reel for reel in self.reels if reel.id == reel_id)
        return None

    def recommend_ad(self, user):
        for ad in self.ads:
            if ad.id not in self.suggested_ads:
                interest_weight = sum(user.interests.get(tag, 0) * user.favourite_tags_count[i]
                                    for i, tag in enumerate(user.interests) if tag in ad.tags)
                self.ad_heap.insert_element(ad.id, interest_weight)

        while True:
            if not self.ad_heap.root:
                self.suggested_ads.clear()
                return self.recommend_ad(user)
            _, ad_id = self.ad_heap.extract_max()
            if ad_id not in self.suggested_ads:
                self.suggested_ads.add(ad_id)
                ad = next((ad for ad in self.ads if ad.id == ad_id), None)
                if ad is not None:
                    return ad

            return None

# The rest of the main loop and setup code remains the same

def main_loop(user, engine):
    ad_shown = False
    while True:
        if not ad_shown and user.reels_watched > 0 and user.reels_watched % 10 == 0:
            current_ad = engine.recommend_ad(user)
            if current_ad:
                print(f"\nAd - ID: {current_ad.id}, Tags: {current_ad.tags}")
                print("\nCommands: Like (L), Dislike (D), Next (N), Quit (Q)")
                action_taken = False
                while not action_taken:
                    user_input = input("Enter your choice: ").strip().upper()
                    if user_input == 'L':
                        print("Liked!")
                        action_taken = True
                    elif user_input == 'D':
                        print("Disliked!")
                        action_taken = True
                    elif user_input == 'N':
                        print("Moving to the next ad.")
                        action_taken = True
                    elif user_input == 'Q':
                        print("Quitting...")
                        return
                ad_shown = True
                continue

        current_reel = engine.recommend_reel(user)
        if not current_reel:
            print("No more available reels.")
            return

        print(f"\nReel - ID: {current_reel.id}, Tags: {current_reel.tags}")
        print("\nCommands: Like (L), Dislike (D), Next (N), Quit (Q)")

        action_taken = False
        watched_time = 0
        while not action_taken:
            start_time = time.time()
            user_input = input("Enter your choice: ").strip().upper()
            if user_input == 'L':
                user.interact(current_reel, 'like')
                print("Liked!")
                action_taken = True
            elif user_input == 'D':
                user.interact(current_reel, 'dislike')
                print("Disliked!")
                action_taken = True
            elif user_input == 'N':
                if watched_time >= 7:
                    user.interact(current_reel, 'watched')
                    print("Watched!")
                print("Moving to the next reel.")
                action_taken = True
            elif user_input == 'Q':
                print("Quitting...")
                return
            end_time = time.time()
            watched_time += end_time - start_time

        ad_shown = False

# Setup
reels = [
    Reel(0, ['funny', 'entertainment', 'comedy']),
    Reel(1, ['drama', 'action', 'thriller']),
    Reel(2, ['science', 'education', 'technology']),
    Reel(3, ['science', 'education', 'technology']),
    Reel(4, ['music', 'dance', 'entertainment']),
    Reel(5, ['travel', 'adventure', 'nature']),
    Reel(6, ['sports', 'fitness', 'health']),
    Reel(7, ['cooking', 'food', 'recipe']),
    Reel(8, ['history', 'documentary', 'education']),
    Reel(9, ['art', 'creative', 'craft']),
    Reel(10, ['news', 'politics', 'current events']),
    Reel(11, ['comedy', 'skit', 'entertainment']),
    Reel(12, ['gaming', 'esports', 'entertainment']),
    Reel(13, ['horror', 'thriller', 'mystery']),
    Reel(14, ['romance', 'love', 'drama']),
    Reel(15, ['pets', 'animals', 'funny']),
    Reel(16, ['technology', 'gadgets', 'innovation']),
    Reel(17, ['finance', 'investing', 'economy']),
    Reel(18, ['motivational', 'inspirational', 'self-help']),
    Reel(19, ['fashion', 'beauty', 'lifestyle']),
    Reel(20, ['DIY', 'how-to', 'tutorial']),
    Reel(21, ['travel', 'vlog', 'exploration']),
    Reel(22, ['mental health', 'self-care', 'wellness']),
    Reel(23, ['environment', 'sustainability', 'nature']),
    Reel(24, ['parenting', 'family', 'relationships']),
    Reel(25, ['animation', 'cartoon', 'fun']),
    Reel(26, ['photography', 'videography', 'creative']),
    Reel(27, ['architecture', 'design', 'creative']),
    Reel(28, ['wildlife', 'conservation', 'nature']),
    Reel(29, ['music', 'instrumental', 'performance']),
    Reel(30, ['mystery', 'suspense', 'detective']),
    Reel(31, ['science fiction', 'fantasy', 'adventure']),
    Reel(32, ['psychology', 'self-help', 'personal development']),
    Reel(33, ['healthcare', 'medicine', 'wellness']),
    Reel(34, ['business', 'entrepreneurship', 'startup']),
    Reel(35, ['automotive', 'cars', 'reviews']),
    Reel(36, ['gardening', 'plants', 'outdoors']),
    Reel(37, ['languages', 'learning', 'education']),
    Reel(38, ['social media', 'trends', 'influencers']),
    Reel(39, ['charity', 'volunteering', 'community']),
    Reel(40, ['dance', 'performance', 'choreography']),
    Reel(41, ['baking', 'pastry', 'desserts']),
    Reel(42, ['mythology', 'legends', 'folklore']),
    Reel(43, ['travel', 'culture', 'exploration']),
    Reel(44, ['martial arts', 'self-defense', 'training']),
    Reel(45, ['cosplay', 'anime', 'conventions']),
    Reel(46, ['nature', 'wildlife', 'adventure']),
    Reel(47, ['sustainability', 'green living', 'environment']),
    Reel(48, ['entrepreneurship', 'startup', 'innovation']),
    Reel(49, ['science', 'technology', 'future']),
    Reel(50, ['fitness', 'workout', 'health']),
    Reel(51, ['cooking', 'recipe', 'home chef']),
    Reel(52, ['history', 'war', 'military']),
    Reel(53, ['art', 'painting', 'drawing']),
    Reel(54, ['news', 'current events', 'analysis']),
    Reel(55, ['comedy', 'stand-up', 'humor']),
    Reel(56, ['gaming', 'strategy', 'reviews']),
    Reel(57, ['thriller', 'mystery', 'suspense']),
    Reel(58, ['romance', 'drama', 'love']),
    Reel(59, ['animals', 'wildlife', 'nature']),
    Reel(60, ['technology', 'innovation', 'gadgets']),
    Reel(61, ['investing', 'finance', 'economy']),
    Reel(62, ['inspiration', 'motivational', 'self-help']),
    Reel(63, ['beauty', 'fashion', 'style']),
    Reel(64, ['how-to', 'DIY', 'craft']),
    Reel(65, ['travel', 'exploration', 'culture']),
    Reel(66, ['mental health', 'wellness', 'self-care']),
    Reel(67, ['family', 'parenting', 'relationships']),
    Reel(68, ['cartoon', 'animation', 'fun']),
    Reel(69, ['videography', 'photography', 'media']),
    Reel(70, ['design', 'architecture', 'creative']),
    Reel(71, ['conservation', 'environment', 'sustainability']),
    Reel(72, ['instrumental', 'music', 'performance']),
    Reel(73, ['detective', 'suspense', 'mystery']),
    Reel(74, ['fantasy', 'science fiction', 'adventure']),
    Reel(75, ['self-help', 'psychology', 'personal development']),
    Reel(76, ['medicine', 'healthcare', 'wellness']),
    Reel(77, ['startup', 'business', 'entrepreneurship']),
    Reel(78, ['cars', 'automotive', 'reviews']),
    Reel(79, ['plants', 'gardening', 'outdoors']),
    Reel(80, ['education', 'learning', 'languages']),
    Reel(81, ['trends', 'social media', 'influencers']),
    Reel(82, ['community', 'volunteering', 'charity']),
    Reel(83, ['performance', 'dance', 'choreography']),
    Reel(84, ['pastry', 'baking', 'desserts']),
    Reel(85, ['legends', 'mythology', 'folklore']),
    Reel(86, ['exploration', 'travel', 'culture']),
    Reel(87, ['self-defense', 'martial arts', 'training']),
    Reel(88, ['anime', 'cosplay', 'conventions']),
    Reel(89, ['urban exploration', 'adventure', 'vlog']),
    Reel(90, ['cryptocurrency', 'finance', 'investing']),
    Reel(91, ['graphic design', 'digital art', 'creative']),
    Reel(92, ['street food', 'travel', 'culture']),
    Reel(93, ['extreme sports', 'adventure', 'fitness']),
    Reel(94, ['science experiments', 'education', 'fun']),
    Reel(95, ['home improvement', 'DIY', 'tutorial']),
    Reel(96, ['pets', 'funny', 'animals']),
    Reel(97, ['theater', 'drama', 'performance']),
    Reel(98, ['book reviews', 'literature', 'reading']),
    Reel(99, ['photography', 'travel', 'adventure']),
    Reel(100, ['holidays', 'travel', 'culture'])
]

ads = [
    Ad(0, ['technology', 'gadgets']),
    Ad(1, ['fashion', 'beauty']),
    Ad(2, ['food', 'restaurants']),
    Ad(3, ['travel', 'vacation']),
    Ad(4, ['cars', 'automotive']),
    Ad(5, ['health', 'fitness']),
    Ad(6, ['finance', 'investing']),
    Ad(7, ['education', 'learning']),
    Ad(8, ['entertainment', 'movies']),
    Ad(9, ['pets', 'animals'])
]

# User interests dictionary (can be modified based on user preferences)
user_interests = {'funny': 1, 'entertainment': 2}

num_reels = len(reels)
user = User(num_reels, user_interests)  # Initialize a single user with the number of reels and interests
engine = RecommendationEngine(reels, ads)

# Run the main loop
main_loop(user, engine)
