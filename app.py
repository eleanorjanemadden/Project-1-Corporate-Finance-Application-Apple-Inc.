"""Thin UI: frozen outputs plus calls to the existing engines."""
import json
from pathlib import Path
import pandas as pd
import streamlit as st
import analysis
import dated_refresh

st.set_page_config(page_title='Apple FCFF workbench',layout='wide')
st.title('Apple | FCFF workbench')
view=st.selectbox('Model basis',['Dated July 31, 2026','Retrospective FY2025 illustration'])
is_dated=view.startswith('Dated')
engine=dated_refresh if is_dated else analysis
path=Path(__file__).parent/'outputs'/('dated' if is_dated else 'retrospective')/'visible_output.json'
if not path.exists():
    st.error('Run python analysis.py and python dated_refresh.py first.');st.stop()
frozen=json.loads(path.read_text());base=frozen['base']
st.caption('FIN43900 | USD millions except USD/share | '+frozen['as_of'])
st.warning(frozen['limitations']);st.write(frozen['decision'])
if is_dated:
    st.write('Dated market price:',frozen['market_price'])
    st.write(frozen['definition'])
st.subheader('Frozen validated result')
st.dataframe(pd.DataFrame([dict(case=k,**v['valuation']) for k,v in frozen['cases'].items()]))

def reset():
    st.session_state['growth_shift']=0.
    st.session_state['margin']=0.

st.sidebar.button('Reset base',on_click=reset,key='reset_base')
shift=st.sidebar.slider('Growth shift each forecast year (percentage points)',-5.,2.,0.,.5,key='growth_shift')
margin=st.sidebar.slider('Gross-margin path shift (percentage points)',-4.,4.,0.,.5,key='margin')
st.sidebar.caption('Judgment stress bounds. Both controls shift the selected annual path. Dated Q4 assumptions stay fixed. Reset restores that model’s full base path, including its nonconstant margins. No forecast is management guidance.')
if abs(margin)>2.:
    st.warning('Margin shift is outside the supplied ±2pp sensitivity range; additional analyst stress.')
gm=base['assumptions']['gross_margin'];gm=[gm]*5 if isinstance(gm,(float,int)) else gm
try:
    selected=dict(base['assumptions'],growth=tuple(g+shift/100 for g in base['assumptions']['growth']),gross_margin=tuple(m+margin/100 for m in gm))
    changed=engine.calculate(selected)
except (ValueError,OverflowError) as error:
    st.error('CHECK FAILED — valuation refused: '+str(error));changed=None
if changed:
    st.success('Accounting, cash floor, FCFF routes and enterprise-equity bridge checks PASS')
    delta=analysis.compare_to_base(changed,base)['value_change']
    st.metric('Selected-basis value / share',f"${changed['valuation']['per_share']:.2f}",f"${delta:+.2f} versus frozen base")
    for title,lines in analysis.model.TABLES:
        keys=[k for _,k in lines];table=[]
        for b,c in zip(base['statements'],changed['statements']):
            table.extend([dict(year=b['year'],case='base',**{k:b[k] for k in keys}),dict(year=c['year'],case='changed',**{k:c[k] for k in keys})])
        with st.expander(title,expanded=title=='Income statement'):st.dataframe(pd.DataFrame(table),hide_index=True)
    st.dataframe(pd.DataFrame([dict(year=r['year'],fcff=r['fcff'],cash_route=r['fcff_cash_route'],nopat=r['nopat'],change_nwc=r['change_nwc']) for r in changed['statements']]))
    with st.expander('Live checks'):st.dataframe(pd.DataFrame(changed['checks']))
st.subheader('Frozen one-at-a-time sensitivity')
st.dataframe(pd.DataFrame(frozen['sensitivity']),hide_index=True)
st.dataframe(pd.DataFrame(frozen['wacc_growth']).pivot(index='wacc',columns='g',values='per_share'))
st.write('Range-dependent rankings:',frozen['rankings'])
with st.expander('Comparables and reverse DCF'):
    st.dataframe(pd.DataFrame(frozen['comparables']));st.json(frozen['reverse_dcf'])
    if is_dated:st.json(frozen['peer_implied'])
    st.caption('One admitted dated platform peer; no mechanical averaging. See docs/comparables.md for screening and definitions.')
st.subheader('Failing-check demonstration — separate copy')
if st.button('Corrupt separate copy and run real check',key='run_demo'):
    st.session_state['demo']=engine.demo_failure()
if 'demo' in st.session_state:
    st.error('DEMONSTRATION CHECK FAILED: '+st.session_state['demo']['caught'])
    st.success('Recovery: untouched valid copy passes the same check. Frozen output unchanged.')
    if st.button('Clear demonstration and recover display',key='clear_demo'):
        del st.session_state['demo'];st.rerun()
st.write(frozen['reversal_trigger'])
st.info('Reported balances and estimated valuation-date amounts are distinct. See docs/completion_status.md for unmet submission requirements. No human review or historical receipt is established here.')
