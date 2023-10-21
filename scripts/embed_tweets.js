fetch('top_tweets.json')
.then(response => response.json())
.then(tweets => {
  let tweetContainer = document.getElementById("tweetContainer");
  tweets.forEach(tweet => {
    let tweetEmbed = document.createElement("div");
    tweetEmbed.innerHTML = tweet.code;
    tweetContainer.appendChild(tweetEmbed);
  });
});
