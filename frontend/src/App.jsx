import { useEffect } from 'react'
import { BrowserRouter as Router } from 'react-router-dom'

function App() {
  useEffect(() => {
    // Initialize auth here if needed
    const initAuth = async () => {
      // Add your auth initialization logic here
    }
    initAuth()
  }, [])

  return (
    <Router>
      <div className="App">
        {/* Add your routes and components here */}
      </div>
    </Router>
  )
}

export default App 