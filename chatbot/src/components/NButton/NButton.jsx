import React from 'react';

const NButton = ({props}) => {
  console.log('NButton props:', props);
  const { btns } = props;

  return (
    <div>
      {btns.map((btn, index) => (
        <button key={index}>{btn.text}</button>
      ))}
    </div>
  );
}

export default NButton;