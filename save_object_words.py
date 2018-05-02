# Other imports.
import dill

class PhysicalObject(object):

	def __init__(self, name, marker_id, word_list):
		self.name = name
		self.marker_id = marker_id
		self.word_list = word_list

	def is_marker_id(self, id):
		return self.marker_id == id

	def get_words(self):
		return self.word_list

def save_object_dict(dict_of_objects):
	with open('object_words.pkl', 'wb') as f:
		dill.dump(dict_of_objects, f)

def load_object_dict():
	return dill.load(open('object_words.pkl','r'))

def main():
	sun = PhysicalObject("sun", 1911, ["round", "yellow", "black", "felt", "fabric", "circle", "abstract", "soft", "tyre", "wheel", "disk", "egg", "heat", "summer", "hot", "weather", "warm", "burn", "beach", "sand", "ocean", "sunburn", "moon", "nova", "star", "space", "planet", "galaxy", "solar system", "solar"])
	leaf = PhysicalObject("leaf", 456, ["leaf", "plant", "green", "tree", "nature", "bug", "stick", "branch", "forest", "flower", "photosynthesis", "salad", "spring", "bloom", "autumn", "fall", "squishy", "fabric", "natural", "bird", "nest", "life", "food", "caterpillar", "soft"])
	red_square = PhysicalObject("red_square", 3616, ["red", "rectangle", "shapes", "circle", "multi-colored", "triangle", "square", "felt", "abstract", "yellow", "blue", "white", "green", "squishy", "pizza", "soft", "toy", "play"])
	toast = PhysicalObject("toast", 249, ["bread", "toast", "food", "sandwich", "loaf", "butter", "jam", "jelly", "breakfast", "flat", "toaster", "warm", "heat", "sandwich", "lettuce", "hungry", "meal"])
	donut = PhysicalObject("donut", 3880, [])
	pineapple = PhysicalObject("pineapple", 500, [])
	squiggle = PhysicalObject("squiggle", 2754, [])
	cube = PhysicalObject("cube", 3326, [])
	vee = PhysicalObject("vee", 2867, [])
	footprint = PhysicalObject("footprint", 275, [])
	fish = PhysicalObject("fish", 1204, [])
	phone = PhysicalObject("phone", 1598, [])

	object_dict = {
		1911:sun,
		456:leaf,
		1911:sun,
		456:leaf,
		3616:red_square,
		249:toast,
		3880:donut,
		500:pineapple,
		2754:squiggle,
		3326:cube,
		2867:vee,
		275:footprint,
		1204:fish,
		159:phone
	}

	save_object_dict(object_dict)

if __name__ == "__main__":
	main()