import React, { Component } from 'react'

class Counter extends Component {
  // YOUR CODE GOES BELOW
  constructor(props) {
    super(props)
    this.state = {count : props.initialValue}
  }
  incrementCounter = () => {
    this.setState({count: this.state.count + 1});
  }
  decrementCounter = () => {
    this.setState({count: this.state.count - 1});

  }
  render() {
    return (
      <div>
        <p>{this.state.count}</p>
        <button onClick= {this.incrementCounter}>Increment Counter</button>
        <button onClick= {this.decrementCounter}>Decrement Counter</button>
      </div>
    )
  }
}

export default Counter
