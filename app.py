#!/usr/bin/env python
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import uuid
import boto3
import json
import base64

THEMES = {
    'AST': Image.open('/app/Banners/LEC_Summer21_Twitter_FanBanner_AST.png'),
    'FNC': Image.open('/app/Banners/LEC_Summer21_Twitter_FanBanner_FNC.png'),
    'G2': Image.open('/app/Banners/LEC_Summer21_Twitter_FanBanner_G2.png'),
    'LEC': Image.open('/app/Banners/LEC_Summer21_Twitter_FanBanner_LEC.png'),
    'MAD': Image.open('/app/Banners/LEC_Summer21_Twitter_FanBanner_MAD.png'),
    'MSF': Image.open('/app/Banners/LEC_Summer21_Twitter_FanBanner_MSF.png'),
    'RGE': Image.open('/app/Banners/LEC_Summer21_Twitter_FanBanner_RGE.png'),
    'S04': Image.open('/app/Banners/LEC_Summer21_Twitter_FanBanner_S04.png'),
    'SK': Image.open('/app/Banners/LEC_Summer21_Twitter_FanBanner_SK.png'),
    'VIT': Image.open('/app/Banners/LEC_Summer21_Twitter_FanBanner_VIT.png'),
    'XL': Image.open('/app/Banners/LEC_Summer21_Twitter_FanBanner_XL.png'),
}


def handler(event, context):
    scenario = json.loads(base64.b64decode(event['body']).decode('utf-8'))
    scenario = event

    image_name = str(uuid.uuid4())
    filename = '{}.png'.format(image_name)
    filepath = '/tmp/{}'.format(filename)
    print('new scenario:')
    print(scenario)
    name = scenario.pop('name')
    fond = THEMES.get(scenario.pop('team'))
    FOND_X = fond.size[0]
    FOND_Y = fond.size[1]
    FONT_SIZE = 100
    draw = ImageDraw.Draw(fond)
    font = ImageFont.truetype('police.otf', FONT_SIZE)
    handle = '@' + name
    w, h = draw.textsize(handle, font=font)
    W, H = int(FOND_X / 2), int(FOND_Y / 2)
    draw.text(((W - w / 2), (H - h / 2)), handle, (255, 255, 255), font=font)
    # fond.show()
    fond.save(filepath, "png")
    print('file generated')
    try:
        s3 = boto3.client('s3')

        with open(filepath, 'rb') as f:
            s3.put_object(Bucket='lkb-chatbots',
                          Key="riot/{}".format(filename),
                          Body=f,
                          ACL='public-read',
                          ContentType='image/png')

        print('file saved')

        response = {
            "statusCode": 200,
            "body": 'https://s3-eu-west-1.amazonaws.com/lkb-chatbots/riot/'
                    '{}'.format(filename)
        }

        return response
    except Exception:
        print('just showing it')
        fond.show()


# if __name__ == '__main__':
#     for theme in THEMES.keys():
#         handler({'name': 'YOURNAMEHERE', 'team': theme}, None)