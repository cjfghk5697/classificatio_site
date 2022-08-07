import {useParams} from 'react-router-dom';
import PredictsList from '../components/PredictsList';

const PredictPage=()=>{
	const params=useParams();
	const pk = params.pk || 'all';
	return (
		<>
			<PredictsList pk={pk}/>
		</>
	);
};

export default PredictPage