import regex as re

# Byte Pair Encoding Tokenizer
class BPE:

    def __init__(self) -> None:
        self.vocab = {}
        self.merges = {}

    def get_stats(self, ids):
        counts = {}
        for pair in zip(ids, ids[1:]):
            counts[pair] = counts.get(pair, 0) + 1
        return counts
    
    def merge(self, ids, pair, idx):
        newids = []
        i = 0
        while i < len(ids):
            if i < len(ids) - 1 and ids[i] == pair [0] and ids[i+1] == pair[1]:
                newids.append(idx)
                i += 2
            else:
                newids.append(ids[i])
                i += 1
        return newids 

    def train(self, text, vocab_size, verbose=False):
        ids = self.encode(text)

        # Generate merges
        num_merges = vocab_size - 256
        for i in range(num_merges):
            stats = self.get_stats(ids)
            pair = max(stats, key=stats.get)
            idx = 256 + i
            if verbose:
                print(f"merging {pair} into a new token {idx}")
            ids = self.merge(ids, pair, idx) 
            self.merges[pair] = idx
        
        # Create vocab from merges: IE: Convert each id to a corresponding token in utf-8
        self.vocab = {idx: bytes([idx]) for idx in range(256)}
        for (p0, p1), idx in self.merges.items():
            self.vocab[idx] = self.vocab[p0] + self.vocab[p1]
    
    def encode(self, text):
        
        tokens = list(text.encode("utf-8"))
        while len(tokens) >= 2:
            stats = self.get_stats(tokens)
            pair = min(stats, key=lambda p: self.merges.get(p, float("inf")))
            if pair not in self.merges:
                break
            idx = self.merges[pair]
            tokens = self.merge(tokens, pair, idx)
        return tokens

    def decode(self, ids):
        # given ids (list of integers), return Python string
        tokens = b"".join(self.vocab[idx] for idx in ids)
        text = tokens.decode("utf-8", errors='replace')
        return text
    

if __name__ == "__main__":
    text = """Mollusca is a phylum of protostomic invertebrate animals, whose members are known as molluscs or mollusks[a] (/ˈmɒləsks/). Around 76,000 extant species of molluscs are recognized, making it the second-largest animal phylum after Arthropoda.[5] The number of additional fossil species is estimated between 60,000 and 100,000,[6] and the proportion of undescribed species is very high. Many taxa remain poorly studied.[7]    Molluscs are the largest marine phylum, comprising about 23% of all the named marine organisms. They are highly diverse, not just in size and anatomical structure, but also in behaviour and habitat, as numerous groups are freshwater and even terrestrial species. The phylum is typically divided into 7 or 8 taxonomic classes,[8] of which two are entirely extinct. Cephalopod molluscs, such as squid, cuttlefish, and octopuses, are among the most neurologically advanced of all invertebrates—and either the giant squid or the colossal squid is the largest known extant invertebrate species. The gastropods (snails, slugs and abalone) are by far the most diverse class and account for 80% of the total classified molluscan species.The four most universal features defining modern molluscs are a soft body composed almost entirely of muscle, a mantle with a significant cavity used for breathing and excretion, the presence of a radula (except for bivalves), and the structure of the nervous system. Other than these common elements, molluscs express great morphological diversity, so many textbooks base their descriptions on a "hypothetical ancestral mollusc" (see image below). This has a single, "limpet-like" shell on top, which is made of proteins and chitin reinforced with calcium carbonate, and is secreted by a mantle covering the whole upper surface. The underside of the animal consists of a single muscular "foot". Although molluscs are coelomates, the coelom tends to be small. The main body cavity is a hemocoel through which blood circulates; as such, their circulatory systems are mainly open. The "generalized" mollusc's feeding system consists of a rasping "tongue", the radula, and a complex digestive system in which exuded mucus and microscopic, muscle-powered "hairs" called cilia play various important roles. The generalized mollusc has two paired nerve cords, or three in bivalves. The brain, in species that have one, encircles the esophagus. Most molluscs have eyes, and all have sensors to detect chemicals, vibrations, and touch. The simplest type of molluscan reproductive system relies on external fertilization, but more complex variations occur. Nearly all produce eggs, from which may emerge trochophore larvae, more complex veliger larvae, or miniature adults. The coelomic cavity is reduced. They have an open circulatory system and kidney-like organs for excretion. Good evidence exists for the appearance of gastropods, cephalopods, and bivalves in the Cambrian period, 541–485.4 million years ago. However, the evolutionary history both of molluscs' emergence from the ancestral Lophotrochozoa and of their diversification into the well-known living and fossil forms are still subjects of vigorous debate among scientists. Fossilized ammonite displayed at the National Museum of the Philippines
    Molluscs have been and still are an important food source for humans. Toxins that can accumulate in certain molluscs under specific conditions create a risk of food poisoning, and many jurisdictions have regulations to reduce this risk. Molluscs have, for centuries, also been the source of important luxury goods, notably pearls, mother of pearl, Tyrian purple dye, and sea silk. Their shells have also been used as money in some preindustrial societies.

    A handful of mollusc species are sometimes considered hazards or pests for human activities. The bite of the blue-ringed octopus is often fatal, and that of Octopus apollyon causes inflammation that can last over a month. Stings from a few species of large tropical cone shells of the family Conidae can also kill, but their sophisticated, though easily produced, venoms have become important tools in neurological research. Schistosomiasis (also known as bilharzia, bilharziosis, or snail fever) is transmitted to humans by water snail hosts, and affects about 200 million people. Snails and slugs can also be serious agricultural pests, and accidental or deliberate introduction of some snail species into new environments has seriously damaged some ecosystems.

    Etymology
    The words mollusc and mollusk are both derived from the French mollusque, which originated from the post-classical Latin mollusca, from mollis, soft, first used by J. Jonston (Historiæ Naturalis, 1650) to describe a group comprising cephalopods.[9] Molluscus is used in classical Latin as an adjective only with nux (nut) to describe a particular type of soft nut. The use of mollusca in biological taxonomy by Jonston and later Linnaeus may have been influenced by Aristotle's τὰ μαλάκια ta malákia (the soft ones; < μαλακός malakós "soft"), which he applied inter alia to cuttlefish.[10][11] The scientific study of molluscs is accordingly called malacology.[12]

    The name Molluscoida was formerly used to denote a division of the animal kingdom containing the brachiopods, bryozoans, and tunicates, the members of the three groups having been supposed to somewhat resemble the molluscs. As now known, these groups have no relation to molluscs, and very little to one another, so the name Molluscoida has been abandoned.[13]

    Definition
    The most universal features of the body structure of molluscs are a mantle with a significant body cavity used for breathing and excretion, and the organization of the nervous system. Many have a calcareous shell.[14]

    Molluscs have developed such a varied range of body structures, finding synapomorphies (defining characteristics) to apply to all modern groups is difficult.[15] The most general characteristic of molluscs is they are unsegmented and bilaterally symmetrical.[16] The following are present in all modern molluscs:[17][19]

    The dorsal part of the body wall is a mantle (or pallium) which secretes calcareous spicules, plates or shells. It overlaps the body with enough spare room to form a mantle cavity.
    The anus and genitals open into the mantle cavity.
    There are paired nerve cords.[18]
    Other characteristics that commonly appear in textbooks have significant exceptions:"""

    bpe = BPE()
    bpe.train(text, 500)

    # Encode
    encode1 = bpe.encode("Hi how are you")
    print(encode1)

    # Decode
    print(bpe.decode(encode1))
