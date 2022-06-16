<script>
    import {Route, Router, Link} from "svelte-navigator";
    import Website from "./website/Website.svelte";
    import MainForm from "./form/MainForm.svelte";
    import NewsForm from "./form/NewsForm.svelte";


</script>
<Router>
    <nav style="    width: 100%;
    display: flex;
    justify-content: space-around; font-size:20px; color:black">
        <Link to="/">Home</Link>
        <Link to="/form">Form</Link>
    </nav>
    <Route path="/" component="{Website}"/>
    <Route path="/form" component="{MainForm}"/>
</Router>
<style>
a:visited{
    text-decoration: none;
    color:black;
}
</style>