from sense_hat import SenseHat

from flask import Flask
from flask_restful import Api, Resource
from flask_restful import reqparse

# Flask
app = Flask(__name__)
api = Api(app)

# SenseHat
sense = SenseHat()


def normalize_var(value, x, y):
    # Clamp between 0 and 100
    value = min(max(value, 0), 100)
    
    # Normalize to [0, 1]:
    value = (value - 0) / 100

    # Then scale to [x, y]:
    rangee = y - x
    return int(value*rangee) + x


class SetMatrix(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('brightness', type=int, help='brightness must be an integer')
        args = parser.parse_args()
        
        count = args["brightness"]
        
        brightness = count
        brightness = normalize_var(brightness, 47, 255)

        leds_list = [[brightness,brightness,brightness] for x in range(64)]
        sense.set_pixels(leds_list)
        
        return {"brightness": brightness}


api.add_resource(SetMatrix, '/api/brightness')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
