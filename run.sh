(
    python apps_bundle_build.py build_bundle;
    cd apps_bundle;
    streamlit run AppBundle.py \
        --server.port ${STREAMLIT_SERVER_PORT} \
	--server.headless true \
	--theme.base dark
)
