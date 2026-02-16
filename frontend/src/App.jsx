import { useEffect, useState } from 'react'

function App() {
  const [expenses, setExpenses] = useState([])

  useEffect(() => {
    // This is the Waiter asking the Python server for food
    fetch("http://127.0.0.1:8000/expenses")
      .then(res => res.json())
      .then(data => setExpenses(data.expenses))
  }, [])

  // --- THE MATH SECTION ---
  // item[1] is the price. We use parseFloat to turn the text into a real number.
  const total = expenses.reduce((acc, item) => {
    return acc + parseFloat(item[1]);
  }, 0);
  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>My Spending Tracker</h1>
      <ul>
        {expenses.map((item, index) => (
          <li key={index}>
            {item[0]}: <strong>${item[1]}</strong> ({item[2] || 'No Category'})
          </li>
        ))}
      </ul>
        {/* --- SHOWING THE TOTAL --- */}
      <div style={{ marginTop: '20px', borderTop: '2px solid #ccc', paddingTop: '10px' }}>
        <h2>Total Spent: <span style={{ color: 'green' }}>${total.toFixed(2)}</span></h2>
      </div>
    </div>
  )
}

export default App