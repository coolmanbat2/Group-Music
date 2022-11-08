import React, { useEffect, useState } from "react";
import { Grid, Button, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { useParams } from "react-router-dom";
import MusicPlayer from "./MusicPlayer";
import CreateRoomPage from "./createRoomPage";

function Room(props) {
  const navigate = useNavigate();
  const [isHost, setIsHost] = useState(false);
  const [guestCanPause, setGuestCanPause] = useState(false);
  const [voteToSkip, setVoteToSkip] = useState(2);
  const [showSettings, setShowSettings] = useState(false);
  const [song, setSong] = useState({});
  const { roomCode } = useParams();

  const getRoomDetails = () => {
    fetch("/api/get-room" + "?code=" + roomCode)
      .then((response) => {
        if (!response.ok) {
          props.clearRoom();
          navigate("/");
        }
        return response.json();
      })
      .then((data) => {
        setVoteToSkip(data.votes_to_skip);
        setGuestCanPause(data.guest_can_pause);
        setIsHost(data.is_host);
      });
    if (isHost) {
      authenticateSpotify();
    }
  };

  // Gets the spotify account.
  function authenticateSpotify() {
    fetch("/api/is-authenicated")
      .then((response) => response.json())
      .then((data) => {
        if (!data.status) {
          fetch("/api/get-auth-url")
            .then((response) => response.json())
            .then((data) => {
              window.location.replace(data.url); // may or may not work in this case.
            });
        }
      });
  }

  function getCurrentSong() {
    fetch("/api/current-song")
      .then((response) => {
        if (!response.ok) {
          return {};
        } else {
          return response.json();
        }
      })
      .then((data) => {
        setSong(data);
      });
  }

  function showSettingsPage() {
    return (
      <Grid container spacing={1}>
        <Grid item xs={12} align="center">
          <CreateRoomPage
            update={true}
            voteToSkip={voteToSkip}
            guestCanPause={guestCanPause}
            roomCode={roomCode}
          />
        </Grid>
        <Grid item xs={12} align="center">
          <Button
            variant="contained"
            color="secondary"
            onClick={() => setShowSettings(false)}
          >
            Close
          </Button>
        </Grid>
      </Grid>
    );
  }

  function RenderSettingsButton() {
    return (
      <Grid item xs={12} align="center">
        <Button
          variant="contained"
          color="primary"
          onClick={() => setShowSettings(true)}
        >
          Settings
        </Button>
      </Grid>
    );
  }

  function leaveButtonPressed() {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    };
    fetch("/api/leave-room", requestOptions).then((_response) => {
      props.clearRoom();
      navigate("/");
    });
  }

  // When webpage loads, retrieve the room details.
  getRoomDetails();
  useEffect(() => {
    getCurrentSong();
  });
  if (showSettings) {
    return showSettingsPage();
  }
  return (
    <React.Suspense fallback="spinner-border">
      <Grid container spacing={1} align="center">
        <Grid item xs={12}>
          <Typography variant="h2">Code: {roomCode}</Typography>
        </Grid>
        {isHost ? RenderSettingsButton() : null}
        <Grid item xs={12}>
          <Button
            variant="contained"
            color="secondary"
            onClick={leaveButtonPressed}
          >
            Leave Room
          </Button>
        </Grid>
      </Grid>
      <Grid item xs={12}>
        <MusicPlayer {...song}/>
      </Grid>
    </React.Suspense>
  );
}

export default Room;
