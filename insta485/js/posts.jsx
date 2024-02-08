import React, { useState, useEffect } from "react";
import InfiniteScroll from "react-infinite-scroll-component";
import Post from "./post";

export default function Posts() {
  const [next, setNext] = useState("");
  const [results, setResults] = useState([]);

  useEffect(() => {
    const url = "/api/v1/posts/";

    fetch(url, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        setNext(data.next);
        setResults(data.results);
      })
      .catch((error) => console.log(error));
  }, []);

  const InfiniteScrollHandle = () => {
    fetch(next, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        setNext(data.next);
        setResults((prevResults) => [...prevResults, ...data.results]);
      })
      .catch((error) => console.log(error));
  };

  return (
    <div>
      <InfiniteScroll
        dataLength={results.length}
        next={InfiniteScrollHandle}
        hasMore={next !== null}
        scrollThreshold={1}
      >
        {results.map((post) => (
          <div key={post.postid}>
            <Post url={post.url} />
          </div>
        ))}
      </InfiniteScroll>
    </div>
  );
}
