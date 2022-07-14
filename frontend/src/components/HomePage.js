import React from 'react';
import CreateRoomPage from "./createRoomPage";
import RoomJoinPage from "./RoomJoin";
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Room from './Room';

function HomePage(props) {
    return (
        <BrowserRouter>
            <Routes>
                <Route path='/' element={
                    <p>hello</p>
                }/>
                <Route path='/join' element={<RoomJoinPage/>}/>
                <Route path='/create' element={<CreateRoomPage/>}/>
                <Route path='/room/:roomCode' element={<Room/>}/>
            </Routes>
        </BrowserRouter>
    );
}

export default HomePage;