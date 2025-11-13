import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

interface UserSummary {
  userId: string
  name: string
  bio: string | null
}

function UserList() {
  const [users, setUsers] = useState<UserSummary[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        setLoading(true)
        const response = await fetch('/api/users')

        if (!response.ok) {
          throw new Error(`Error fetching users: ${response.status}`)
        }

        const data = await response.json()
        setUsers(data)
        setError(null)
      } catch (err) {
        console.error('Error fetching users:', err)
        setError(err instanceof Error ? err.message : 'Unknown error')
      } finally {
        setLoading(false)
      }
    }

    fetchUsers()
  }, [])

  if (loading) {
    return (
      <div className="loading">
        <p>Loading users...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="error">
        <p>Error: {error}</p>
      </div>
    )
  }

  if (users.length === 0) {
    return (
      <div className="empty">
        <p>No users found.</p>
      </div>
    )
  }

  return (
    <div className="user-list">
      <h1>Social OS Wiki</h1>
      <p className="subtitle">User Profiles</p>

      <div className="users-grid">
        {users.map((user) => (
          <Link
            key={user.userId}
            to={`/users/${user.userId}`}
            className="user-card"
          >
            <h2>{user.name}</h2>
            {user.bio && <p className="bio">{user.bio}</p>}
            <span className="user-id">@{user.userId}</span>
          </Link>
        ))}
      </div>
    </div>
  )
}

export default UserList
