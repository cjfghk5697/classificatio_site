
const PercentBarItem=({sub_pred,sub_result})=>{
	const width_size=`width:${sub_result}`
	return (
		<>
		{sub_result}
		<div className="h-3 relative max-w-xl rounded-full overflow-hidden">
			<div className="w-full h-full bg-gray-200 absolute"></div>
			<div className="h-full bg-green-500 absolute" style={width_size}></div>
		</div>
		</>
	);
};

const PercentBar=({data})=>{
	const sub_pred=data.sub_pred
	const sub_result=data.sub_result
	return(
	<>


		{sub_result.map((arr,index)=>(
			<PercentBarItem key={index} sub_result={arr} sub_pred={sub_pred[index-1]}/>
		))}
	</>
	)
}
export default PercentBar