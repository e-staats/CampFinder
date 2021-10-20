import React from 'react'

export interface Props{
    text: string,
    onClick: React.MouseEventHandler<HTMLButtonElement>
}

function Button({text, onClick}: Props) {
return(
    <button type="button" onClick={onClick} >{text}</button>
)
}

export default Button