from backend.ai.__init__ import *
from backend.config import *

FILE_PATH = r'frontend/static/images/ai-images/blogs/'
FILE_PATH_AVATAR = r'frontend/static/images/ai-images/avatars/'

class ImageGeneration():
    def __init__(self):
        pass
    
    def get_ai_image(self, description):
        # get the response from the OpenAI API
        response = openai.Image.create(
            prompt="Generate a digital image for a blog post with the following description: " + description,
            n=1,
            size="1024x1024",
        )
        # save the image to the server
        name = self.save_image(response['data'][0]['url'])
        return FILE_PATH + name
    
    def get_ai_avatar(self, name):
        response = openai.Image.create(
            prompt="Generate a digital image for a user with the following name: " + name,
            n=1,
            size="256x256",
        )
        print(response['data'][0]['url'])
        name = self.save_image(response['data'][0]['url'], file_path=True)
        return FILE_PATH_AVATAR + name
    
    def save_image(self, url, file_path=None):
        # get image unique directory
        directory = self.check_dir((FILE_PATH_AVATAR + self.generate_name() + '.png'), file_path=True) if file_path else self.check_dir((FILE_PATH + self.generate_name() + '.png'))
        # get url data
        img_data = requests.get(url).content
        # save image to directory
        with open(directory, 'wb') as handler:
            handler.write(img_data)
        if file_path:
            return directory.split(FILE_PATH_AVATAR)[1]
        return directory.split(FILE_PATH)[1]
    
    def generate_name(self, length=50):
        # generate a random name for the image
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
    
    def check_dir(self, directory, file_path=None):
        # check if the directory exists
        if os.path.exists(directory): 
            return self.check_dir((FILE_PATH + self.generate_name() + '.png')) if file_path == None else self.check_dir((FILE_PATH_AVATAR + self.generate_name() + '.png'), file_path=True)
        return directory