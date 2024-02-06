import moviepy.editor as mpe
import moviepy.video.fx.all as vfx


def combine_audio(vidname, audname, outname, fps=5):
    clip = mpe.VideoFileClip(vidname)
    # Modify the FPS
    clip = clip.set_fps(clip.fps / 50)

    # Apply speed up
    clip = clip.fx(vfx.speedx, 1/50)
    # print("fps: {}".format(final.fps))

    # Save video clip
    audio_background = mpe.AudioFileClip(audname)
    breakpoint()
    final_clip = clip.set_audio(audio_background)
    final_clip.write_videofile(outname, fps=fps)

combine_audio("0cbb2ac2-5c4d-4b17-834e-647cfd378d01.mp4", "data/podcast_output.mp3", "data/output.mp4") # i create a new file
# combine_audio("test.mp4", "test.mp3", "test.mp4") # i rewrite on the same file```