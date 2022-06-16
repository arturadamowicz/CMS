<script>
    import NewsForm from "./NewsForm.svelte";

    const data_json = (async () => {
        const response = await fetch('http://127.0.0.1:5000/data')
        return await response.json()
    })()

    data_json.then((d)=>FormNet.json = d)

    import HeaderForm from "./HeaderForm.svelte";
    import SliderForm from "./SliderForm.svelte";
    import {FormNet} from "../net";

</script>
{#await data_json}
    Loading...
{:then data}
    <HeaderForm formNet={FormNet} headerData = {data.header}></HeaderForm>
    <SliderForm formNet={FormNet} sliderData={data.content.slider}></SliderForm>
    <NewsForm formNet={FormNet} newsData={data.content.news}></NewsForm>
    <button on:load = {()=>{FormNet.json = data}} on:click={()=>FormNet.updateData()}>UPDATE</button>
{/await}