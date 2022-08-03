import React, { useEffect, useState } from "react";
import CreateRoomPage from "./createRoomPage";
import RoomJoinPage from "./RoomJoin";
import { BrowserRouter, Routes, Route, Link, Navigate } from "react-router-dom";
import { Grid, Button, ButtonGroup, Typography } from "@mui/material";
import Room from "./Room";

function renderHomePage() {
  return (
    <Grid container spacing={3}>
      <Grid item xs={12} align="center">
        <Typography variant="h3" compact="h3">
          House Party (From Spongebob)
        </Typography>
      </Grid>
      <Grid item xs={12} align="center">
        {/* Sets up a horizontal line of buttons */}
        <ButtonGroup disableElevation variant="contained" color="primary">
          <Button color="primary" to="/join" component={Link}>
            Join A Room!
          </Button>
          <Button color="secondary" to="/create" component={Link}>
            Create A Room!
          </Button>
        </ButtonGroup>
      </Grid>
    </Grid>
  );
}

function HomePage(props) {
  const [roomCode, setRoomCode] = useState(null);
  useEffect(() => {
    async function autoEnter() {
      fetch("/api/user-in-room")
        .then((response) => response.json())
        .then((data) => {
          setRoomCode(data.code);
        });
    }
    autoEnter();
  });
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={
             roomCode ? (
              <Navigate to={`/room/${roomCode}`} />
            ) : (
              renderHomePage()
            )
          }
        />
        <Route path="/join" element={<RoomJoinPage />} />
        <Route path="/create" element={<CreateRoomPage />} />
        <Route path="/room/:roomCode" element={<Room />} />
      </Routes>
    </BrowserRouter>
  );
}

export default HomePage;
