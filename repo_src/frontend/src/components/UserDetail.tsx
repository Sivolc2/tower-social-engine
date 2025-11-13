import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'

interface User {
  userId: string
  name: string
  bio: string | null
  wikiContent: string | null
  createdAt?: string
  updatedAt?: string
}

function UserDetail() {
  const { userId } = useParams<{ userId: string }>()
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchUser = async () => {
      if (!userId) {
        setError('No user ID provided')
        setLoading(false)
        return
      }

      try {
        setLoading(true)
        const response = await fetch(`/api/users/${userId}`)

        if (!response.ok) {
          throw new Error(`Error fetching user: ${response.status}`)
        }

        const data = await response.json()
        setUser(data)
        setError(null)
      } catch (err) {
        console.error('Error fetching user:', err)
        setError(err instanceof Error ? err.message : 'Unknown error')
      } finally {
        setLoading(false)
      }
    }

    fetchUser()
  }, [userId])

  if (loading) {
    return (
      <div className="loading">
        <p>Loading user profile...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="error">
        <Link to="/" className="back-link">&larr; Back to Users</Link>
        <p>Error: {error}</p>
      </div>
    )
  }

  if (!user) {
    return (
      <div className="error">
        <Link to="/" className="back-link">&larr; Back to Users</Link>
        <p>User not found</p>
      </div>
    )
  }

  return (
    <div className="user-detail">
      <Link to="/" className="back-link">&larr; Back to Users</Link>

      <header className="user-header">
        <h1>{user.name}</h1>
        <span className="user-id">@{user.userId}</span>
        {user.bio && <p className="bio">{user.bio}</p>}
      </header>

      {user.wikiContent && (
        <div className="wiki-content">
          <ReactMarkdown>{user.wikiContent}</ReactMarkdown>
        </div>
      )}

      {!user.wikiContent && (
        <p className="empty">No additional information available.</p>
      )}

      {(user.createdAt || user.updatedAt) && (
        <footer className="user-footer">
          {user.createdAt && (
            <p className="meta">Created: {new Date(user.createdAt).toLocaleDateString()}</p>
          )}
          {user.updatedAt && (
            <p className="meta">Updated: {new Date(user.updatedAt).toLocaleDateString()}</p>
          )}
        </footer>
      )}
    </div>
  )
}

export default UserDetail
