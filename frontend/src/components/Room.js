import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

function Room(props) {
  const [isHost, setIsHost] = useState(false);
  const [guestCanPause, setGuestCanPause] = useState(false);
  const [voteToSkip, setVoteToSkip] = useState(2);
  const { roomCode } = useParams();

  const getRoomDetails = () => {
    fetch("/api/get-room" + "?code=" + roomCode)
      .then((response) => response.json())
      .then((data) => {
        setVoteToSkip(data.votes_to_skip);
        setGuestCanPause(data.guest_can_pause);
        setIsHost(data.is_host);
      });
  };

  // When webpage loads, retrieve the room details.
  useEffect(() => {
    getRoomDetails()
  });
  return (
    <React.Suspense fallback="spinner-border">
      <h3>{roomCode}</h3>
      <p>Host: {isHost.toString()}</p>
      <p>Guest Can Pause: {guestCanPause.toString()}</p>
      <p>Vote To Skip: {voteToSkip.toString()}</p>
    </React.Suspense>
  );
}

export default Room;
