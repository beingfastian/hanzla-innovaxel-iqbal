'use client'
import { useState } from 'react'
import styles from '../styles/Home.module.css'

export default function Home() {
  const [url, setUrl] = useState('')
  const [shortCode, setShortCode] = useState('')
  const [result, setResult] = useState<null | {
    id: string
    url: string
    shortCode: string
    createdAt: string
    updatedAt: string
    accessCount?: number
  }>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
  
    try {
      const response = await fetch('http://127.0.0.1:8000/api/shorten/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ original_url: url })
      })
      const data = await response.json()
  
      if (response.ok) {
        setResult({
          id: data.id,
          url: data.url,
          shortCode: data.short_code,
          createdAt: new Date(data.created_at).toLocaleString(),
          updatedAt: new Date(data.updated_at).toLocaleString(),
        })
        setShortCode(data.short_code)
      } else {
        setError(data.detail || 'Something went wrong')
      }
    } catch (error: any) {
      setError(`Network Error: ${error.message}`)
    }
  
    setLoading(false)
  }

  const handleRetrieve = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/${shortCode}/`)
      const data = await response.json()
      if (response.ok) {
        setResult({
          id: data.id,
          url: data.url,
          shortCode: data.shortCode,
          createdAt: new Date(data.createdAt).toLocaleString(),
          updatedAt: new Date(data.updatedAt).toLocaleString(),
        })
      } else {
        setError(data.detail || 'Short code not found')
      }
    } catch (error: any) {
      setError(`Network Error: ${error.message}`)
    }
  }

  const handleUpdate = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/${shortCode}/update/`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ original_url: url })
      })
      const data = await response.json()
      if (response.ok) {
        setResult({
          id: data.id,
          url: data.url,
          shortCode: data.short_code,
          createdAt: new Date(data.created_at).toLocaleString(),
          updatedAt: new Date(data.updated_at).toLocaleString(),
        })
      } else {
        setError(data.detail || 'Update failed')
      }
    } catch (error: any) {
      setError(`Network Error: ${error.message}`)
    }
  }

  const handleDelete = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/${shortCode}/delete/`, {
        method: 'DELETE'
      })
      if (response.ok) {
        setResult(null)
        setShortCode('')
      } else {
        setError('Delete failed')
      }
    } catch (error: any) {
      setError(`Network Error: ${error.message}`)
    }
  }

  const handleStats = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/${shortCode}/stats/`)
      const data = await response.json()
      if (response.ok) {
        setResult({
          id: data.id,
          url: data.url,
          shortCode: data.short_code,
          createdAt: new Date(data.created_at).toLocaleString(),
          updatedAt: new Date(data.updated_at).toLocaleString(),
          accessCount: data.access_count
        })
      } else {
        setError(data.detail || 'Stats retrieval failed')
      }
    } catch (error: any) {
      setError(`Network Error: ${error.message}`)
    }
  }

  return (
    <main className={styles.main}>
      <div className={styles.container}>
        <h1 className={styles.title}>URL Shortener</h1>
        
        <form onSubmit={handleSubmit} className={styles.form}>
          <input
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Enter your long URL"
            required
            className={styles.input}
          />
          <button type="submit" className={styles.button} disabled={loading}>
            {loading ? 'Shortening...' : 'Shorten'}
          </button>
        </form>

        <input
          type="text"
          value={shortCode}
          onChange={(e) => setShortCode(e.target.value)}
          placeholder="Enter short code"
          className={styles.input}
        />
        <div className={styles.actions}>
          <button onClick={handleRetrieve} className={styles.button}>Retrieve</button>
          <button onClick={handleUpdate} className={styles.button}>Update</button>
          <button onClick={handleDelete} className={styles.button}>Delete</button>
          <button onClick={handleStats} className={styles.button}>Get Stats</button>
        </div>

        {result && (
          <div className={styles.result}>
            <p><strong>ID:</strong> {result.id}</p>
            <p><strong>Original URL:</strong> {result.url}</p>
            <p><strong>Short Code:</strong> {result.shortCode}</p>
            <p><strong>Created At:</strong> {result.createdAt}</p>
            <p><strong>Updated At:</strong> {result.updatedAt}</p>
            {result.accessCount !== undefined && (
              <p><strong>Access Count:</strong> {result.accessCount}</p>
            )}
          </div>
        )}

        {error && (
          <div className={styles.error}>
            <p>{error}</p>
          </div>
        )}
      </div>
    </main>
  )
}
