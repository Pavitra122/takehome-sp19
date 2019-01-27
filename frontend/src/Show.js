import React, { Component } from 'react'
import Counter from './Counter'

class Show extends Component {
  // YOUR CODE GOES BELOW
  constructor(props) {
    super(props)
  }
  render() {
    return (
      <div>
          <p>{this.props.name}</p>
          <Counter initialValue={this.props.episodes_seen}/>
      </div>


    )
  }
}

export default Show
