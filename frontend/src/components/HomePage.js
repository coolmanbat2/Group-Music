import React from 'react';
import CreateRoomPage from "./createRoomPage";
import RoomJoinPage from "./RoomJoin";
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

function HomePage(props) {
    return (
        <BrowserRouter>
            <Routes>
                <Route path='/' element={
                    <p>hello</p>
                }/>
                <Route path='/join' element={<RoomJoinPage/>}/>
                <Route path='/create' element={<CreateRoomPage/>}/>
            </Routes>
        </BrowserRouter>
    );
}

export default HomePage;