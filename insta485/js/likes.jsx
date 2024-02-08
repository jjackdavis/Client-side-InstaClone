import React from "react";
import PropTypes from "prop-types";

export default function Likes({ like, setLikes, postid }) {
  function handleLikes() {
    // Update the state immediately before making the fetch request
    setLikes((prevLikes) => ({
      numLikes: prevLikes.numLikes + (like.lognameLikesThis ? -1 : 1),
      lognameLikesThis: !like.lognameLikesThis,
      url: null,
    }));

    if (like.lognameLikesThis) {
      fetch(like.url, { method: "DELETE", credentials: "same-origin" })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
        })
        .catch((error) => console.log(error));
    } else {
      fetch(`/api/v1/likes/?postid=${postid}`, {
        method: "POST",
        credentials: "same-origin",
      })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          setLikes((prevLikes) => ({
            ...prevLikes,
            url: data.url,
          }));
        })
        .catch((error) => console.log(error));
    }
  }

  return (
    postid !== 0 && (
      <>
        {like.numLikes} {like.numLikes === 1 ? "like   " : "likes   "}
        <button
          data-testid="like-unlike-button"
          type="button"
          onClick={handleLikes}
        >
          {like.lognameLikesThis ? "unlike" : "like"}
        </button>
      </>
    )
  );
}

Likes.propTypes = {
  like: PropTypes.shape({
    url: PropTypes.string,
    lognameLikesThis: PropTypes.bool.isRequired,
    numLikes: PropTypes.number.isRequired,
  }).isRequired,
  setLikes: PropTypes.func.isRequired,
  postid: PropTypes.number.isRequired,
};
