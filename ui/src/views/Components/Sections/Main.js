import React from "react";
// plugin that creates slider
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Switch from "@material-ui/core/Switch";
// @material-ui/icons
// core components
import GridContainer from "components/Grid/GridContainer.js";
import GridItem from "components/Grid/GridItem.js";
import Button from "components/CustomButtons/Button.js";
import ReactPlayer from "react-player";
import myVideo from "assets/videos/robin_final_cut.mp4";
import TextField from "@material-ui/core/TextField";

import triggerProcessing from "requests.js";
// import CustomLinearProgress from "components/CustomLinearProgress/CustomLinearProgress";

import styles from "assets/jss/material-kit-react/views/componentsSections/basicsStyle.js";

const useStyles = makeStyles(styles);

export default function Main() {
  const useStateWithLocalStorage = (localStorageKey) => {
    const [value, setValue] = React.useState(
      localStorage.getItem(localStorageKey) || ""
    );
    React.useEffect(() => {
      localStorage.setItem(localStorageKey, value);
    }, [value]);
    return [value, setValue];
  };
  const classes = useStyles();
  const [summarize, setSummarize] = React.useState(false);
  const [article, setArticle] = React.useState("");
  const [loading, setLoading] = React.useState(false);
  const [loaded, setLoaded] = useStateWithLocalStorage("loaded");
  const [videoURL, setVideoURL] = useStateWithLocalStorage("videoURL");

  const trigger = () => {
    setLoaded(false);
    setLoading(true);
    console.log(article);
    console.log(summarize);
    triggerProcessing(article, summarize).then((data) => {
      setLoading(false);
      setVideoURL(data["url"]);
      setLoaded(true);
    });
  };

  return (
    <div className={classes.sections}>
      <div className={classes.container}>
        <div className={classes.title}>
          <h2>Why DeepFakeNews?</h2>
          <h3 className={classes.subtitle}>
            Create videos and share them to your audience with few clicks by
            simply providing the article.
          </h3>
        </div>
        <ReactPlayer
          url={myVideo}
          controls={true}
          width={"100%"}
          height={"100%"}
        />
      </div>
      <div className={classes.container}>
        <div id="try_it">
          <div className={classes.title}>
            <h2>Try It Out!</h2>
          </div>
          <GridContainer>
            <GridItem xs={12} sm={6} md={6} lg={6}>
              <TextField
                id="outlined-multiline-static"
                label="Article"
                multiline
                fullWidth
                rows={4}
                value={article}
                onChange={(event) => setArticle(event.target.value)}
              />
              <div>
                <FormControlLabel
                  control={
                    <Switch
                      checked={summarize}
                      onChange={(event) => setSummarize(event.target.checked)}
                      value="checkedA"
                      classes={{
                        switchBase: classes.switchBase,
                        checked: classes.switchChecked,
                        thumb: classes.switchIcon,
                        track: classes.switchBar,
                      }}
                    />
                  }
                  classes={{
                    label: classes.label,
                  }}
                  label="Summarize"
                />
              </div>
            </GridItem>
            <Button color="primary" round onClick={() => trigger()}>
              {loading ? "Generating" : "Generate"}
            </Button>
          </GridContainer>
        </div>
      </div>
      {loaded && (
        <div className={classes.container}>
          <div className={classes.title}>
            <h2>See the result</h2>
          </div>
          <ReactPlayer
            url={videoURL}
            controls={true}
            width={"100%"}
            height={"100%"}
          />
        </div>
      )}
    </div>
  );
}
