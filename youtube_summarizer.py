import os
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = "your_openai_api_key"

def get_video_transcript(video_id):
    """Fetches the transcript of a YouTube video."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([entry["text"] for entry in transcript])
        return transcript_text
    except Exception as e:
        return f"Error fetching transcript: {e}"

def summarize_transcript(transcript_text):
    """Summarizes the transcript using OpenAI's GPT model."""
    llm = ChatOpenAI(model_name="gpt-4", temperature=0.5)
    
    messages = [
        SystemMessage(content="You are an AI assistant that summarizes YouTube video transcripts."),
        HumanMessage(content=f"Summarize the following transcript:\n{transcript_text}")
    ]
    
    summary = llm(messages)
    return summary.content

def main():
    video_url = input("Enter YouTube Video URL: ")
    video_id = video_url.split("v=")[-1]  # Extract Video ID from URL
    
    print("\nFetching transcript...")
    transcript_text = get_video_transcript(video_id)

    if "Error" in transcript_text:
        print(transcript_text)
        return
    
    print("\nGenerating summary...")
    summary = summarize_transcript(transcript_text)

    print("\nVideo Summary:")
    print(summary)

if __name__ == "__main__":
    main()
