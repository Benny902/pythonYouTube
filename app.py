from flask import Flask, render_template, request, send_file
from pytube import YouTube
import OS


app = Flask(__name__, static_url_path='/static')
port = int(os.environ.get('PORT', 5000))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        # Retrieve video link and download type from the form
        video_link = request.form['video_link']
        download_type = request.form['download_type']
        
        # Download video or audio based on the selected type
        yt = YouTube(video_link)
        if download_type == 'Download Video':
            stream = yt.streams.get_highest_resolution()
        elif download_type == 'Download Audio':
            stream = yt.streams.get_audio_only()
        else:
            raise ValueError('Invalid download type')
        
        # Set the Content-Disposition header to force download
        return send_file(stream.download(), as_attachment=True)
    except Exception as e:
        message = f'An error occurred: {str(e)}'
        return render_template('result.html', message=message)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=port)
