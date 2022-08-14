import React, { useState } from "react";
import {
  Button,
  Grid,
  Typography,
  TextField,
  FormHelperText,
  FormControl,
  Radio,
  RadioGroup,
  FormControlLabel,
  Collapse,
  Alert,
} from "@mui/material";
import { Link, useNavigate } from "react-router-dom";
import GetCookie from "./GetCookie";

function CreateRoomPage(props) {
  const navigate = useNavigate();
  const [guestCanPause, setGuestCanPause] = useState(props.guestCanPause);
  const [voteToSkip, setVoteToSkip] = useState(props.voteToSkip);
  const [message, setMessage] = useState("");
  const [isError, setIsError] = useState(false);

  function handleVotesChange(e) {
    setVoteToSkip(e.target.value);
  }

  function handleGuestCanPauseChange(e) {
    setGuestCanPause(e.target.value === "playpause" ? true : false);
  }

  function handleRoomButtonPressed() {
    const csrfToken = GetCookie();
    const requestOptions = {
      method: "POST",
      headers: { "Content-type": "application/json", "X-CSRFToken": csrfToken },
      body: JSON.stringify({
        votes_to_skip: voteToSkip,
        guest_can_pause: guestCanPause,
      }),
    };
    fetch("/api/create-room", requestOptions)
      .then((response) => response.json())
      .then((data) => navigate("/room/" + data.code));
  }

  function handleUpdateButtonPressed() {
    const csrfToken = GetCookie();
    const requestOptions = {
      method: "PATCH",
      headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken },
      body: JSON.stringify({
        votes_to_skip: voteToSkip,
        guest_can_pause: guestCanPause,
        code: props.roomCode,
      }),
    };
    fetch("/api/update-room", requestOptions).then((response) => {
      if (response.ok) {
        setMessage("Successfully updated room.");
        setIsError(false);
      } else {
        setMessage("Unsucessfully updated room. Error: " + response.statusText);
        setIsError(true);
      }
    });
  }

  function renderCreateButtons() {
    return (
      <Grid container spacing={1}>
        <Grid item xs={12} align="center">
          <Button
            color="primary"
            variant="contained"
            onClick={handleRoomButtonPressed}
          >
            Create A Room
          </Button>
        </Grid>
        <Grid item xs={12} align="center">
          <Button color="secondary" variant="contained" to="/" component={Link}>
            Back
          </Button>
        </Grid>
      </Grid>
    );
  }

  function renderUpdateButtons() {
    return (
      <Grid item xs={12} align="center">
        <Button
          color="primary"
          variant="contained"
          onClick={handleUpdateButtonPressed}
        >
          Update Room
        </Button>
      </Grid>
    );
  }

  const title = props.update ? "Update Room" : "Create a Room";
  const severity = isError ? "error" : "success";

  return (
    <Grid container spacing={1}>
      <Grid item xs={12} align="center">
        <Collapse in={message != ""}>
          <Alert
            onClose={() => {
              setMessage("");
            }}
            variant="filled"
            severity={severity}
          >
            {message}
          </Alert>
        </Collapse>
      </Grid>
      <Grid item xs={12} align="center">
        <Typography component="h4" variant="h4">
          {title}
        </Typography>
      </Grid>
      <Grid item xs={12} align="center">
        <FormControl component="fieldset">
          <FormHelperText component="div">
            <div align="center">Guest Control of Playback state</div>
          </FormHelperText>
          <RadioGroup
            row
            defaultValue={props.guestCanPause ? "playpause" : "nocontrol"}
            onChange={handleGuestCanPauseChange}
          >
            <FormControlLabel
              value="playpause"
              control={<Radio color="primary" />}
              label="Play/Pause"
              labelPlacement="bottom"
            />
            <FormControlLabel
              value="nocontrol"
              control={<Radio color="secondary" />}
              label="No Control"
              labelPlacement="bottom"
            />
          </RadioGroup>
        </FormControl>
      </Grid>
      <Grid item xs={12} align="center">
        <FormControl>
          <TextField
            required={true}
            type="number"
            defaultValue={voteToSkip}
            inputProps={{
              min: 1,
              style: { textAlign: "center" },
            }}
            onChange={handleVotesChange}
          />
          <FormHelperText component="div">
            <div align="center">Votes Required To Skip Song</div>
          </FormHelperText>
        </FormControl>
      </Grid>
      {props.update ? renderUpdateButtons() : renderCreateButtons()}
    </Grid>
  );
}

CreateRoomPage.defaultProps = {
  update: false,
  voteToSkip: 2,
  guestCanPause: true,
  roomCode: null,
};

export default CreateRoomPage;
