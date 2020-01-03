import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import numpy as np
import tld as tld_parser

base_domains = [
	"github.com",
	"openu.ac.il",
	"haaretz.com",
	"pytorch.com",
	"wikipedia.org"
]

def text2ndarray(word):
	MAX_WORD_SIZE = 32
	dummy_string = "a" * MAX_WORD_SIZE
	dim3_size = 3 # For RGB. If we move to RGBA, change to 4

	PADDING_SIZE = 1
	if len(word) > MAX_WORD_SIZE:
		raise Exception("WORD TOO LONG")

	bgcolor = "#FFF"
	text_color = "#000"
	font = ImageFont.load_default()
	max_word_size_in_font_width, max_word_size_in_font_height = font.getsize(dummy_string)

	img_width = max_word_size_in_font_width + PADDING_SIZE + PADDING_SIZE
	img_height = max_word_size_in_font_height * 2
	# img_height = img_width # If we want a square

	img = Image.new("RGB", (img_width, img_height), bgcolor)
	draw = ImageDraw.Draw(img)
	w, h = draw.textsize(word)

	draw.text(((img_width-w)/2,(img_height-h)/2), word, text_color, font=font)
	img.save("test.png")
	pic_as_np_ndarray = np.array(img.getdata()).reshape(img.size[0], img.size[1], dim3_size)
	return pic_as_np_ndarray


class FakeDomainGenerator(object):
	def __init__(self):
		self.permutations_dictionay = {
			"a": ["4"],
			# "b": ["d"],
			# "d": ["b"],
			"e": ["3"],
			"i": ["l", "1"],
			"l": ["i", "1"],
			"m": ["nn"],
			"o": ["0"],
			"s": ["5"],
			"w": ["vv"]
		}
	
	def get_fake_domain(self, seed):
		"""
		Given a real domain, generate a fake version of it by doing some weird permutations
		"""
		seed = seed.lower()
		seed_with_http = "http://" + seed
		seed_domain_after_tld_parsing = tld_parser.parse_tld(seed_with_http)
		tld, domain, _ = seed_domain_after_tld_parsing # ignoring subdomain for now

		permutable_chars_in_word = [c for c in domain if c in self.permutations_dictionay]
		if len(permutable_chars_in_word) == 1:
			n_of_obfuscations = 1
		else:
			n_of_obfuscations = np.random.randint(1, len(permutable_chars_in_word))

		chars_to_obfuscate = np.random.choice(permutable_chars_in_word, n_of_obfuscations, replace=False)
		# print("chars_to_obfuscate = ", chars_to_obfuscate)

		new_domain = ""
		for c in domain:
			if c in chars_to_obfuscate:
				new_char = np.random.choice(self.permutations_dictionay[c], 1)[0]
				new_domain += new_char
			else:
				new_domain += c
		
		return "{new_domain}.{tld}".format(new_domain=new_domain, tld=tld)
		

fake_generator = FakeDomainGenerator()

fake_domains = {}
for domain in base_domains:
	if domain not in fake_domains:
		fake_domains[domain] = set()
	
	for i in range(5):
		randomly_generated_domain = fake_generator.get_fake_domain(domain)
		fake_domains[domain].add(randomly_generated_domain)

print(fake_domains)
# fake_domain = f.get_fake_domain("bluevoyant.com")
# print("fake_domain = " + fake_domain)
# text2ndarray("bluevoyant.com")

