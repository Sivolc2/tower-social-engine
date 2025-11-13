import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './styles/App.css'
import UserList from './components/UserList'
import UserDetail from './components/UserDetail'

function App() {
  return (
    <Router>
      <div className="container">
        <Routes>
          <Route path="/" element={<UserList />} />
          <Route path="/users/:userId" element={<UserDetail />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
