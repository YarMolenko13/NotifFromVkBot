import requests
from datetime import datetime
import os
import time
# https://api.vk.com/method/METHOD_NAME?PARAMETERS&access_token=ACCESS_TOKEN&v=V 

# response = requests.get(ourRequest)
# data = response.json()


class WallParse:
	def test(self, domain):
		token = 'e78fcf8bd932159b6f651898d6971c685ae23138417c94ba1151e3396dc098a26c304b49e0f7ecc53e8f1'
		version = 5.122
		response = requests.get('https://api.vk.com/method/wall.get',
								params = {
									'count':1,
									'access_token': token,
									'v': version,
									'domain': domain
								})
		json = response.json()

		try:
			item = json['response']['items'][0]['owner_id']
			if item == 306432714:
				return True
		except:
			print('invalid domain')
			return False


	'''получаем данные'''
	def get_data(self, domain):

		# получаем json
		def get_json_data(self, offset=0):
			method = 'wall.get'
			token = 'e78fcf8bd932159b6f651898d6971c685ae23138417c94ba1151e3396dc098a26c304b49e0f7ecc53e8f1'
			version = 5.122
			user_id = '306432714'

			response = requests.get('https://api.vk.com/method/{}'.format(method),
									params = {
										'count':1,
										'offset': offset,
										'access_token': token,
										'v': version,
										'domain': domain
									})
			json_response = response.json()
			return json_response

		item = get_json_data(domain)['response']['items'][0]

		try:
			if item['is_pinned']:
				item = get_json_data(domain, offset=1)['response']['items'][0]
		except:
			pass

		try:
			id_post = item['id']
		except:
			id_post = ''

		try:
			timestamp = item['date']
			date = datetime.fromtimestamp(timestamp).strftime('%d %b %H:%M')
		except:
			date = ''

		try:
			text = item['text']
		except:
			text = ''

		img_list = []
		video_list = []

		# print(item)

		if 'attachments' in item:
			# фото
			for at in item['attachments']:
				type = at['type']
				if type == 'photo':
					img = at['photo']['sizes'][-1]['url']
					img_list.append(img)

			# видео
			for at in item['attachments']:
				type = at['type']
				if type == 'video':
					owner_id = at['video']['owner_id']
					id = at['video']['id']
					video = str(owner_id) + '_' + str(id)
					video_url = 'https://vk.com/video' + video
					video_list.append(video_url)

			# for at in item['attachments']:
			# 	type = at['type']
			# 	if type == 'audio':
			# 		print(at['audio'])

		# print(img_list)
		# print(video_list)

		data = {
			'id_post': id_post,
			'date': date,
			'text': text,
			'img_list': img_list,
			'video_list': video_list
		}
		
		return data

	'''получаем имя паблика'''
	def get_pub_name(self, domain):
		token = 'e78fcf8bd932159b6f651898d6971c685ae23138417c94ba1151e3396dc098a26c304b49e0f7ecc53e8f1'
		version = 5.122
		user_id = '306432714'
		
		response = requests.get('https://api.vk.com/method/groups.getById',
								params = {
									'count': 1,
									'group_id': domain,
									'access_token': token,
									'v': version
								})
		json = response.json()
		print(json)
		name = json['response'][0]['name']
		return name


	'''скачиваем картинку'''
	def download_img(self, url_img):
		try:
			r = requests.get(url_img, stream=True)
	
			with open('img.jpg', 'bw') as f:
				for chunk in r.iter_content(8192):
					f.write(chunk)
		except:
			print('Error url img')
			try:
				os.remove('img.jpg')
			except:
				pass
			pass


p = WallParse()
p.get_data('neewschool')
# print(p.get_pub_name('howdyho_net'))
# p.test('neggcvxblk34553465476564yiojdsjhg')
