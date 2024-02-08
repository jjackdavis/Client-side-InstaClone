import React, { useState } from "react";
import PropTypes from "prop-types";

export default function Comments({ comments, setComments, postid }) {
  const [textEntry, setTextEntry] = useState("");

  const handleCommentAdd = (event) => {
    setTextEntry("");
    // You can pass formData as a fetch body directly:
    fetch(`/api/v1/comments/?postid=${postid}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: textEntry }),
      credentials: "same-origin",
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // Update comments state
        const commentEntry = {
          commentid: data.commentid,
          lognameOwnsThis: true,
          owner: data.owner,
          ownerShowUrl: `/users/${data.owner}/`,
          text: data.text,
          url: `/api/v1/comments/${data.commentid}/`,
        };
        console.log(commentEntry);
        setComments((prevComments) => [
          ...prevComments,
          {
            commentid: data.commentid,
            lognameOwnsThis: true,
            owner: data.owner,
            ownerShowUrl: `/users/${data.owner}/`,
            text: data.text,
            url: `/api/v1/comments/${data.commentid}/`,
          },
        ]);
      })
      .catch((error) => console.log(error));
    event.preventDefault();
  };

  const handleChange = (event) => {
    setTextEntry(event.target.value);
  };

  function handleCommentDelete(comment) {
    setComments((prevComments) =>
      prevComments.filter(
        (comments1) => comments1.commentid !== comment.commentid,
      ),
    );
    fetch(comment.url, { method: "DELETE", credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .catch((error) => console.log(error));
  }

  function CommentsList() {
    const listItems = comments.map((comment) => (
      <div key={comment.commentid}>
        <a href={comment.ownerShowUrl}>{comment.owner}</a> {comment.text}
        {comment.lognameOwnsThis && (
          <button
            type="button"
            data-testid="delete-comment-button"
            onClick={() => handleCommentDelete(comment)}
            style={{ marginLeft: "10px" }}
          >
            Delete
          </button>
        )}
      </div>
    ));
    return listItems;
  }

  return (
    postid !== 0 && (
      <>
        <div data-testid="comment-text">
          <CommentsList />
        </div>
        <form data-testid="comment-form" onSubmit={handleCommentAdd}>
          Comment:
          <input
            className="ui input"
            type="text"
            value={textEntry}
            onChange={handleChange}
          />
        </form>
      </>
    )
  );
}

Comments.propTypes = {
  comments: PropTypes.arrayOf(
    PropTypes.shape({
      commentid: PropTypes.number.isRequired,
      lognameOwnsThis: PropTypes.bool.isRequired,
      owner: PropTypes.string.isRequired,
      ownerShowUrl: PropTypes.string.isRequired,
      text: PropTypes.string.isRequired,
      url: PropTypes.string.isRequired,
    }),
  ).isRequired,
  setComments: PropTypes.func.isRequired,
  postid: PropTypes.number.isRequired,
};
