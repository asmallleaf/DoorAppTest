from .createapp import createapp

app = createapp('development')

if __name__ == '__main__':
    app.run()
