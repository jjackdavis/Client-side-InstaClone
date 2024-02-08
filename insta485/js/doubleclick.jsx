export default function handleDoubleClick(like, setLikes, postid) {
  if (like.lognameLikesThis) {
    return;
  }

  setLikes((prevLikes) => ({
    numLikes: prevLikes.numLikes + 1,
    lognameLikesThis: !like.lognameLikesThis,
    url: null,
  }));

  // Now, make the fetch request
  fetch(`/api/v1/likes/?postid=${postid}`, {
    method: "POST",
    credentials: "same-origin",
  })
    .then((response) => {
      if (!response.ok) throw Error(response.statusText);
    })
    .catch((error) => console.log(error));
}
