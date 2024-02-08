import React, { useState, useEffect } from "react";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import utc from "dayjs/plugin/utc";
import PropTypes from "prop-types";
import Likes from "./likes";
import Comments from "./comments";
import handleDoubleClick from "./doubleclick";

// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
export default function Post({ url }) {
  dayjs.extend(relativeTime);
  dayjs.extend(utc);

  /* Display image and post owner of a single post */
  const [imgUrl, setImgUrl] = useState("");
  const [owner, setOwner] = useState("");
  const [comments, setComments] = useState([
    {
      commentid: 0,
      lognameOwnsThis: false,
      owner: "",
      ownerShowUrl: "",
      text: "",
      url: "",
    },
  ]);
  const [created, setCreated] = useState("");
  const [likes, setLikes] = useState({
    lognameLikesThis: false,
    numLikes: 0,
    url: "",
  });
  const [ownerImgUrl, setOwnerImgUrl] = useState("");
  const [ownerShowUrl, setOwnerShowUrl] = useState("");
  const [postid, setPostid] = useState(0);
  const [finishedRender, setFinishedRender] = useState(false);
  // const [url, setUrl] = useState("");

  useEffect(() => {
    // Declare a boolean flag that we can use to cancel the API request.
    let ignoreStaleRequest = false;

    // Call REST API to get the post's information
    fetch(url, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // If ignoreStaleRequest was set to true, we want to ignore the results of the
        // the request. Otherwise, update the state to trigger a new render.
        if (!ignoreStaleRequest) {
          setImgUrl(data.imgUrl);
          setOwner(data.owner);
          setComments(data.comments);
          setCreated(data.created);
          setLikes(data.likes);
          setOwnerImgUrl(data.ownerImgUrl);
          setOwnerShowUrl(data.ownerShowUrl);
          setPostid(data.postid);
        }
      })
      .then(() => {
        setFinishedRender(true);
      })
      .catch((error) => console.log(error));

    return () => {
      // This is a cleanup function that runs whenever the Post component
      // unmounts or re-renders. If a Post is about to unmount or re-render, we
      // should avoid updating state.
      ignoreStaleRequest = true;
    };
  }, [url]);

  // Render post image and post owner
  return (
    finishedRender && (
      <div className="post">
        <div className="post-title" style={{ textAlign: "left" }}>
          <a href={ownerShowUrl}>
            <img src={ownerImgUrl} alt="" className="profile-pic" />
          </a>
          <span style={{ float: "right" }}>
            <a href={`/posts/${postid}/`}>
              {dayjs.utc(created).local().fromNow()}
            </a>
          </span>
          <div
            style={{
              textAlign: "center",
              color: "red",
              fontSize: "30px",
              padding: "10px",
            }}
          >
            <a href={ownerShowUrl}>{owner}</a>
          </div>
        </div>
        <div style={{ textAlign: "center" }}>
          <img
            src={imgUrl}
            alt="post_image"
            onDoubleClick={() => handleDoubleClick(likes, setLikes, postid)}
          />
        </div>
        <div className="post-info">
          <Likes like={likes} setLikes={setLikes} postid={postid} />
          <Comments
            comments={comments}
            setComments={setComments}
            postid={postid}
          />
        </div>
      </div>
    )
  );
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};
